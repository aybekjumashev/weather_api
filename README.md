# Hawa Rayı API

Bul Hawa Rayı API Django hám Django Rest Framework járdeminde islenip shıǵılǵan. Ol paydalanıwshılarǵa berilgen qala ushın haqıyqıy waqıttaǵı hawa rayı maǵlıwmatların alıw imkaniyatın beredi hám sırtqı API shaqırıwların kemeytiw ushın alınǵan maǵlıwmatlardı bazaǵa saqlaydı.

## Imkaniyatları
- Sırtqı API járdeminde hawa rayı maǵlıwmatların alıw
- 30 minut dawamında maǵlıwmatlardı keshlew
- Paydalanıwshıǵa tiyisli lokatsiyalardı belgilew

## Ornatıw
### Talaplar
- Python 3.8+
- Django 4+
- PostgreSQL (majburiy emes, biraq usınıs etiledi)

### Ornatıw Boyınsha Qollanba
1. Repozitoriydı klonlaw:
   ```bash
   git clone https://github.com/aybekjumashev/weather-api.git
   cd weather-api
   ```
2. Virtual ortalıqtı jaratıw hám aktivlestiriw:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows'ta `venv\Scripts\activate` qollanıń
   ```
3. Kitapxanalardı ornatıw:
   ```bash
   pip install -r requirements.txt
   ```
4. Ózgeriwshilerdi sazlaw:
   `.env` faylın jaratıń hám tómendegilerdi qosıń:
   ```env
   DATABASE_URL=postgres://user:password@localhost:5432/weatherdb
   WEATHER_API_KEY=sizdiń_api_gilteńiz_bul_jerde
   DEBUG=True
   ```
5. Migratsiyalardı qollanıw:
   ```bash
   python manage.py migrate
   ```
6. Superpaydalanıwshını jaratıw (majburiy emes):
   ```bash
   python manage.py createsuperuser
   ```
7. Serverdi iske túsiriw:
   ```bash
   python manage.py runserver
   ```

## API Hújjetleri
API-den paydalanıw boyınsha hújjetler: [Postman](https://documenter.getpostman.com/view/25343078/2sAYdoDmxH)

## Qollanılǵan Texnologiyalar
- Django hám Django REST Framework
- PostgreSQL
- Sırtqı Hawa Rayı API (OpenWeatherMap)



