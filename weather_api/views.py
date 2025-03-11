from rest_framework import generics, permissions, status
from .serializers import RegistrationationSerializer, LoginSerializer, UserUpdateSerializer, WeatherSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound
from .models import User, WeatherData
from rest_framework.response import Response
from django.conf import settings
from django.utils.timezone import now, localtime, timedelta
from .weather_client import WeatherClient
from django.core.exceptions import ObjectDoesNotExist

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegistrationationSerializer
    permission_classes = [permissions.AllowAny]

class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  

class WeatherAPIView(generics.GenericAPIView):
    serializer_class = WeatherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, city):
        weather_client = WeatherClient(settings.OPENWEATHERMAP_API_KEY, user_agent="weather_api")

        try:
            lat, lon = None, None

            if request.user.city != city:
                corrected_city, lat, lon = weather_client.city_corrector.correct_city_name(city)
                if corrected_city:
                    city = corrected_city
                else:
                    return Response(
                        {"detail": "Qala atı durıs kiritilmegen."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            try:
                weather_data = WeatherData.objects.get(city=city)
                created = False
            except ObjectDoesNotExist:
                weather_data = WeatherData(city=city, temp=0, desc="", humidity=0, speed=0, current_time=now(), latitude=request.user.latitude, longitude=request.user.longitude)
                weather_data.save()
                created = True

            time_difference = now() - localtime(weather_data.current_time)
            if created or time_difference > timedelta(minutes=30):
                print(f'UPDATING WEATHER dt={time_difference} created={created}')

                if weather_data.latitude and weather_data.longitude:
                    lat, lon = weather_data.latitude, weather_data.longitude
                elif lat is not None and lon is not None:
                    weather_data.latitude = lat
                    weather_data.longitude = lon
                    weather_data.save()
                else:
                    return Response(
                        {"detail": "Geokode qáteligi"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if lat is not None and lon is not None:
                    api_data = weather_client.get_weather_by_coordinates(lat, lon)

                    if api_data:
                        weather_data.temp = api_data['temp']
                        weather_data.desc = api_data['desc']
                        weather_data.humidity = api_data['humidity']
                        weather_data.speed = api_data['speed']
                        weather_data.current_time = now()
                        weather_data.save()
                    else:
                        return Response(
                            {"detail": "hawa rayı maǵlıwmatları tabılmadı."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE,  
                        )
                else:
                    return Response(
                        {"detail": "Koordinata maǵlıwmatları joq."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            weather_data_dict = {
                'city': weather_data.city,
                'temp': weather_data.temp,
                'desc': weather_data.desc,
                'humidity': weather_data.humidity,
                'speed': weather_data.speed,
            }

            serializer = self.get_serializer(data=weather_data_dict)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)

        except Exception as e:
            print(f"Error in get_weather_data: {e}")
            return Response(
                {"detail": "Server qátesi"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )