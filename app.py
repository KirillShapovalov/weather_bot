from flask import request, render_template, redirect, url_for
import requests
from . import create_app
import os
import json
from .models import User, get_session
# import telebot
# from telebot import types


# bot = telebot.TeleBot(os.environ.get('TG_TOKEN'))

# sys.path.append('/Users/kirill/PycharmProjects/weather_bot/')


session = get_session()

app = create_app()


def get_weather():
    params = {
        'lat': 55.75396,
        'lon': 37.620393,
    }
    header = {
        'X-Yandex-API-Key': os.environ.get('YA_TOKEN'),
        # 'X-Yandex-API-Key': 'a270ee02-7ba9-4a56-8a59-80e4fb5b9a99',
    }
    api_result = requests.get('https://api.weather.yandex.ru/v2/forecast/', params, headers=header)
    api_response = api_result.json()
    return f"Сейчас в Москве {api_response['fact']['temp']} градусов"


def send_greeting_message(chat_id, username):
    method = "sendMessage"
    token = os.environ.get('TG_TOKEN')
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {
        "chat_id": chat_id,
        "text": f'Привет, {username}!'
    }
    requests.post(url, data=data)


def send_weather_message(chat_id, text):
    method = "sendMessage"
    token = os.environ.get('TG_TOKEN')
    # token = '5372114457:AAGrhSeD1eUGrKu1Ank-di5K83PWarDmPy4'
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {
        'chat_id': chat_id,
        'text': text,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "Red",
                        "callback_data": "Red"
                    },
                    {
                        "text": "Blue",
                        "callback_data": "Blue"
                    },
                    {
                        "text": "Green",
                        "callback_data": "Green"
                    }
                ]
            ]
        }
        # 'reply_markup':
        #     {
        #         'inline_keyboard': [
        #             [
        #                 {
        #                     'text': 'Получить погоду в Москве',
        #                     "callback_data": text
        #                 }
        #             ]
        #         ]
        #     }
    }
    requests.post(url, data=data)


@app.route('/register')
def register_user():
    return render_template('register.html')


# @bot.message_handler(command=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, f'Я погодабот, приятно познакомитсья, {message.from_user.first_name}')

@app.route('/', methods=['POST'])
def receive_update():
    if request.method == "POST":
        if request.json["message"]["text"] == '/start':

            chat_id = request.json["message"]["chat"]["id"]
            send_weather_message(chat_id, get_weather())
        return {"ok": True}
    #         username = request.json["message"]["chat"]["username"]
    #         users_list_id = session.query(User.chat_id).all()
    #         if chat_id in users_list_id:
    #             send_greeting_message(chat_id=chat_id, username=username)
    #             weather = get_weather()
    #             send_weather_message(chat_id, weather)
    #
    #         send_weather_message(chat_id=chat_id)
    #     print(request.json)
    #     chat_id = request.json["message"]["chat"]["id"]
    #
    #
    #     else:
    #         username = request.json["message"]["chat"]["username"]
    #         new_user = User().fill(chat_id=chat_id, username=username)
    #         session.add(new_user)
    #         session.commit()
    #         session.close()
    #         redirect(url_for('register_user'))
    # return {"ok": True}
