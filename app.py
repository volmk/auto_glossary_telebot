import os

from flask import Flask, request
from fake_useragent import UserAgent

import telebot
from glossary import get_span, get_form_file

TOKEN = '880907439:AAFnvUJtDKAKmQRAaEkYeUrMVkIkrUHj7ws'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Отправь сообщение вида "<code>{get_form_file()}</code>"', parse_mode='html')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')
    ua = UserAgent()

    words_str = message.text
    res = ""
    for idx, s in enumerate(words_str.split(', ')):
        gloss = get_span(s.translate({' ': '%20'}), ua.ie)
        line = f'{idx + 1}. {s} – {gloss}\n'
        res += line
        bot.send_chat_action(cid, 'typing')
        if idx+1 % 10 == 0:
            bot.send_message(cid, f'Обработано слов: {idx+1}')
        if idx+1 % 30 == 0:
            bot.send_message(cid, res)
            res = ''

    bot.send_message(cid, res)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://tranquil-cove-07309.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run()
