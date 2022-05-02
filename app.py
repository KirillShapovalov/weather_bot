import json

from flask import request
import requests
from . import create_app
import os
from .models import User, get_session
from sqlalchemy import select

session = get_session()

app = create_app()


def get_weather():
    params = {
        'lat': 55.75396,
        'lon': 37.620393,
    }
    header = {
        'X-Yandex-API-Key': os.environ.get('YA_TOKEN'),
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
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {
        'chat_id': chat_id,
        'text': text,
    }
    requests.post(url, data=data)


def send_weather_button(chat_id, text):
    method = "sendMessage"
    token = os.environ.get('TG_TOKEN')
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {
        'chat_id': chat_id,
        'text': 'Погода в Москве',
        'reply_markup': json.dumps({'inline_keyboard': [[{
            'text': 'Получить погоду',
            'url': text
        }]]})
    }
    requests.post(url, data=data)


@app.route('/', methods=['POST'])
def receive_update():
    if request.method == "POST":
        if request.json["message"]["text"] == '/start':
            chat_id = request.json["message"]["chat"]["id"]
            send_weather_message(chat_id, get_weather())
            users_list_id = session.scalars(select(User.chat_id)).all()
            if chat_id in users_list_id:
                pass
            else:
                username = request.json["message"]["chat"]["username"]
                new_user = User().fill(chat_id=chat_id, username=username)
                session.add(new_user)
                session.commit()
                session.close()
        return {"ok": True}
