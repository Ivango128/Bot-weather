import requests
from dotenv import load_dotenv, find_dotenv
import os

import pandas as pd
import matplotlib.pyplot as plt

load_dotenv(find_dotenv())
token = os.getenv('token')

def get_temperature(lat, lon):
    # URL для запроса погоды
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"

    # Отправляем запрос к API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Получаем текущую температуру (последний час в данных)
        #current_temp = str(data['current']['temperature_2m']) + ' Давление' + str(data['current']['pressure_msl']) + ' Т2 ' + str(data['current']['apparent_temperature'])

        df = pd.DataFrame(data["hourly"])

        # Convert time to datetime
        df["time"] = pd.to_datetime(df["time"])

        # Plotting the data
        #plt.figure(figsize=(10, 5))
        plt.plot(df["time"], df["temperature_2m"], marker='o', linestyle='-', color='b')
        plt.title('Hourly Temperature Forecast')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot as an image file
        plt.savefig('hourly_temperature_forecast.png')


        return #current_temp
    else:
        print(f"Ошибка: {response.status_code}")
        return None

#sdasdasda
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot(token, parse_mode = 'HTML')

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = KeyboardButton(text="Отправить геопозицию", request_location=True)
    markup.add(button_geo)
    bot.send_message(message.chat.id, "Пожалуйста, отправьте свою геопозицию.", reply_markup=markup)

# Обработка геопозиции
@bot.message_handler(content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    temperature = get_temperature(latitude, longitude)
    bot.send_photo(message.chat.id, open('hourly_temperature_forecast.png', 'rb'))
    #bot.send_message(message.chat.id, f"Спасибо! Погода сейчас {temperature}")

# Запуск бота
bot.polling()



