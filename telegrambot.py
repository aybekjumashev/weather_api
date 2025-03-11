import requests
import time

BOT_TOKEN = "5624330397:AAGFy0D1p-WpW7xymb6mc5ffS2R3SEy4yOM"
API_BASE_URL = "https://weatherapi.up.railway.app/api"  
# API_BASE_URL = "http://localhost:8000/api" 


def get_or_create_user(telegram_id):
    headers = {'Content-Type': 'application/json'}
    payload = {"username": f"User-{telegram_id}", "password": f"Pass-{telegram_id}"}

    # Login 
    login_url = f"{API_BASE_URL}/auth/login/"
    response = requests.post(login_url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data

    # Register
    register_url = f"{API_BASE_URL}/auth/register/"
    response = requests.post(register_url, headers=headers, json={**payload, "password2": payload["password"]})
    if response.status_code == 201:
        data = requests.post(login_url, headers=headers, json=payload).json() 
        return data

    return None  

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?timeout=10"
    if offset:
        url += f"&offset={offset}"
    response = requests.get(url)
    return response.json()

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=payload)
    return response.json()

def handle_message(update):
    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        text = message.get('text')
        user = get_or_create_user(chat_id)

        if user is None:
            send_message(chat_id, "Dizimnen ótiwde qátelik júz berdi.")
            return

        access_token = user['access']
        user_data = user['user_data']
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'} 

        if text:
            if text == '/start':
                answer = "Assalawma aleykum!\n/setcity {qala} buyrıǵı arqalı qalańızdı belgileń.\n/weather buyrıǵı arqalı hawa rayı maǵlıwmatların kóriń."
                send_message(chat_id, answer)

            elif text.startswith('/setcity'):
                try:
                    city = text.split()[1]
                    city = city.title()
                    data = {'city': city}
                    rest_api_url = f"{API_BASE_URL}/users/city/" 
                    response = requests.patch(rest_api_url, headers=headers, json=data) 

                    if response.status_code == 200:
                        data = response.json()
                        corrected_city = f' ({data['city']})'
                        if data['city'] == city:
                            corrected_city = ''
                        answer = f"{city}{corrected_city} qalası belgilendi!"
                    else:
                        answer = f"Qátelik júz berdi: {response.status_code}"

                    send_message(chat_id, answer)
                except IndexError:
                    answer = "Nadurıs format. /setcity {qala} kórinisinde jazıń."
                    send_message(chat_id, answer)
                except requests.exceptions.RequestException as e:
                    answer = f"API ge soraw jiberiwde qátelik: {e}"
                    send_message(chat_id, answer)

            elif text == '/weather':
                try:
                    city = user_data['city']
                    if city:
                        city = city.title()
                        weather_api_url = f"{API_BASE_URL}/weather/{city}/"
                        weather_response = requests.get(weather_api_url, headers=headers)
                        if weather_response.status_code == 200:
                            weather_data = weather_response.json()
                            corrected_city = f' ({weather_data['city']})'
                            if weather_data['city'] == city:
                                corrected_city = ''
                            answer = f"{city}{corrected_city} qalası hawa rayı:\n\nTemperatura: {weather_data['temp']}\nHalı: {weather_data['desc']}\nÍǵallıq: {weather_data['humidity']}\nSamal tezligi: {weather_data['speed']}"
                        else:
                            answer = f"Hawa rayı maǵlıwmatları tabılmadı."
                    else:
                        answer = "Qala belgilenbegen. Iltimas, /setcity {qala} buyrıǵı arqalı qalańızdı belgileń."
                    send_message(chat_id, answer)
                except requests.exceptions.RequestException as e:
                    answer = f"API ge soraw jiberiwde qátelik: {e}"
                    send_message(chat_id, answer)

            elif text.startswith('/weather'):
                try:
                    city = text.split()[1]
                    city = city.title()
                    weather_api_url = f"{API_BASE_URL}/weather/{city}/"
                    weather_response = requests.get(weather_api_url, headers=headers)
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        corrected_city = f' ({weather_data['city']})'
                        if weather_data['city'] == city:
                            corrected_city = ''
                        answer = f"{city}{corrected_city} qalası hawa rayı:\n\nTemperatura: {weather_data['temp']}\nHalı: {weather_data['desc']}\nÍǵallıq: {weather_data['humidity']}\nSamal tezligi: {weather_data['speed']}"
                    else:
                        answer = f"Hawa rayı maǵlıwmatları tabılmadı."
                    send_message(chat_id, answer)
                except IndexError:
                    answer = "Nadurıs format. /weather {qala} kórinisinde jazıń."
                    send_message(chat_id, answer)
                except requests.exceptions.RequestException as e:
                    answer = f"APIga so'rov yuborishda xatolik: {e}"
                    send_message(chat_id, answer)
            else:
                answer = "Túsiniksiz buyrıq."
                send_message(chat_id, answer)

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if 'result' in updates:
            for update in updates['result']:
                handle_message(update)
                offset = update['update_id'] + 1
        # time.sleep(1)

if __name__ == '__main__':
    main()