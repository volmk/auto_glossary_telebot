import os

from flask import Flask, request

import telebot
from glossary import write_glossary, get_form_file

TOKEN = '880907439:AAFnvUJtDKAKmQRAaEkYeUrMVkIkrUHj7ws'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Отправь сообщение вида "<code>{get_form_file()}</code>"', parse_mode='html')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')
    glossary = write_glossary(message.str)
    bot.send_message(cid, glossary)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https:///tranquil-cove-07309.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run()