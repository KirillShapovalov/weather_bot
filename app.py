from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from flask import request
import requests
import os
from .models import User, get_session
from sqlalchemy import select
import telebot
from telebot.apihelper import set_webhook, delete_webhook, get_webhook_info
from telebot import types


app = Flask(__name__)
tg_token = os.environ.get('TG_TOKEN')
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(tg_token)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@db/weather_db'
db.init_app(app)
session = get_session()


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    users_list_id = session.scalars(select(User.chat_id)).all()
    if chat_id in users_list_id:
        markup = types.ReplyKeyboardMarkup()
        button = types.KeyboardButton('/get_weather')
        markup.add(button)
        bot.send_message(
            message.chat.id,
            text='Нажмите, чтобы получить прогноз',
            reply_markup=markup
        )
    else:
        markup = types.ReplyKeyboardMarkup()
        button = types.KeyboardButton('/register')
        markup.add(button)
        bot.send_message(
            message.chat.id,
            text='Нажмите, чтобы зарегистрироваться в боте',
            reply_markup=markup
        )


@bot.message_handler(commands=['register'])
def register(message):
    chat_id = message.chat.id
    username = message.chat.username
    new_user = User().fill(chat_id=chat_id, username=username)
    session.add(new_user)
    session.commit()
    session.close()
    markup = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton('/get_weather')
    markup.add(button)
    bot.send_message(
        message.chat.id,
        text='Вы успешно зарегистрированы. Нажмите на кнопку, чтобы получить прогноз',
        reply_markup=markup
    )


@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    params = {
        'lat': 55.75396,
        'lon': 37.620393,
    }
    header = {
        'X-Yandex-API-Key': os.environ.get('YA_TOKEN'),
    }
    api_result = requests.get('https://api.weather.yandex.ru/v2/forecast/', params, headers=header)
    api_response = api_result.json()
    bot.send_message(
        message.chat.id,
        text=f"Сейчас в Москве {api_response['fact']['temp']} градусов"
    )


@app.route("/", methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route('/setwebhook', methods=['GET', 'POST'])
def webhook():
    delete_webhook(token=tg_token, drop_pending_updates=True)
    set_webhook(token=tg_token, url='https://1f46-95-24-28-52.eu.ngrok.io/', drop_pending_updates=True)
    return get_webhook_info(token=tg_token)
