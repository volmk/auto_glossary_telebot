import telebot

from modules.glossary import Glossary
from modules.reducers import Reducers

import os

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')

_bot = telebot.TeleBot(token)

start_msg = 'Доступні команди:\n/en\n' \
            'Але ми працюємо над покращенням :)'


@_bot.message_handler(commands=['en'])
def en(message):
    text = message.text[3:]
    if not text:
        _bot.send_message(message.chat.id,
                          'Для пошуку англійських слів відправ повідомлення типу\n'
                          '<code>/en first, second, third</code>\n'
                          'Вони обов\'язково мають бути розділені комою з пробілом',
                          parse_mode='html', disable_web_page_preview=True)
    else:
        send_dict(message, text, Reducers.create, 'Пошук англійських слів')


@_bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    _bot.send_message(message.chat.id, start_msg, parse_mode='html')


def send_dict(message, words_str, reducer, first_msg):
    cid = message.chat.id

    def normalize(word):
        return word.strip(' ,.:\n').capitalize()

    words_arr = sorted(map(normalize, words_str.split(', ')))

    _bot.send_message(cid, first_msg, disable_web_page_preview=True)
    _bot.send_message(cid, f'Отримано слів: {len(words_arr)}')
    _bot.send_chat_action(cid, 'typing')

    glossary = Glossary(reducer)
    res = ''
    words_in_message = 0
    for idx, s in enumerate(words_arr, 1):
        words_in_message += 1
        word = s.translate({' ': '%20'})
        res += glossary.create_html(word, idx)

        if idx % 5 == 0:
            _bot.send_chat_action(cid, 'typing')

        if words_in_message % 20 == 0 or len(res) > 3500:
            words_in_message = 0
            _bot.send_message(cid, res, parse_mode='html')
            _bot.send_chat_action(cid, 'typing')
            res = ''

    _bot.send_message(cid, res, parse_mode='html')
    _bot.send_message(cid, start_msg)


class BotConfig:
    @staticmethod
    def process_updates(req):
        _bot.process_new_updates([telebot.types.Update.de_json(req)])

    @staticmethod
    def set_webhook(url):
        _bot.remove_webhook()
        _bot.set_webhook(url=url)
