import telebot
from telebot.apihelper import ApiException

import os

from dotenv import load_dotenv

from modules.glossary.controller import Controller
from modules.glossary.model_eng import ModelEng
from modules.glossary.model_ger import ModelGer
from modules.glossary.view import ViewHtml

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
MEDIA_CHAT = os.getenv('MEDIA_CHAT')
DEV_MODE = os.getenv('DEV_MODE')

_bot = telebot.TeleBot(TOKEN)


def api_err_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApiException as e:
            if DEV_MODE:
                print(func.__name__)
                print(e)
            try:
                _bot.send_message(MEDIA_CHAT, func.__name__ + str(e))
            except ApiException:
                pass
            return None

    return wrapper


@api_err_wrapper
def __send_msg(uid, text, **options):
    _bot.send_message(uid, text, **options)


def __send_info(msg):
    __send_msg(MEDIA_CHAT,
               f'<a href="tg://user?id={msg.from_user.id}">{msg.from_user.first_name}</a>\n\n'
               f'{msg.text}',
               parse_mode='html')


@_bot.message_handler(commands=['en'])
def en(message):
    __send_info(message)
    cid = message.chat.id
    text = message.text[3:]
    if not text:
        __send_msg(cid,
                   'Для пошуку англійських слів відправ повідомлення типу\n\n'
                   '<code>/en first, second, third</code>\n\n'
                   'Вони обов\'язково мають бути розділені комою',
                   parse_mode='html')
    else:
        def normalize(worrd):
            return worrd.strip(' ,.:\n').capitalize()

        words_arr = sorted(map(normalize, text.split(',')))
        controller = Controller(ModelEng(), ViewHtml())
        send_dict(cid, 'Англійська', controller, words_arr)


@_bot.message_handler(commands=['ge'])
def ge(message):
    __send_info(message)
    cid = message.chat.id
    text = message.text[3:]
    if not text:
        __send_msg(cid,
                   'Для пошуку німецьких слів відправ повідомлення типу\n\n'
                   '<code>/ge Erster, Klatsch, random</code>\n\n'
                   'Вони обов\'язково мають бути розділені комою',
                   parse_mode='html')
    else:
        def normalize(worrd):
            return worrd.strip(' ,.:\n').capitalize()

        words_arr = sorted(map(normalize, text.split(',')))
        controller = Controller(ModelGer(), ViewHtml())
        send_dict(cid, 'Німецька', controller, words_arr)


@_bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    __send_info(message)
    __send_start_info(message.chat.id)


def __send_start_info(cid):
    __send_msg(cid,
               'Доступні команди:\n'
               '/en - англійська | dictionary.cambridge.org\n'
               '/ge - німецька | duden.de\n'
               'Але ми працюємо над покращенням :)',
               disable_web_page_preview=True)


@api_err_wrapper
def send_dict(cid, lang, controller, words_arr):
    __send_msg(cid, f'{lang} | Отримано слів: {len(words_arr)}')
    _bot.send_chat_action(cid, 'typing')

    res = ''
    words_in_message = 0
    for idx, s in enumerate(words_arr, 1):
        words_in_message += 1
        word = s.translate({' ': '%20'})
        res += controller.create(word, idx)

        if idx % 5 == 0:
            _bot.send_chat_action(cid, 'typing')

        if words_in_message % 20 == 0 or len(res) > 3500:
            words_in_message = 0
            __send_msg(cid, res, parse_mode='html')
            _bot.send_chat_action(cid, 'typing')
            res = ''

    __send_msg(cid, res, parse_mode='html')
    __send_start_info(cid)


class BotConfig:
    @staticmethod
    def process_updates(req):
        _bot.process_new_updates([telebot.types.Update.de_json(req)])

    @staticmethod
    def set_webhook(url):
        _bot.remove_webhook()
        _bot.set_webhook(url=url)
