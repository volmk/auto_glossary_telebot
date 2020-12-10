import telebot
from telebot.apihelper import ApiException

from modules.glossary import Glossary
from modules.reducers import Reducers

import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
MEDIA_CHAT = os.getenv('MEDIA_CHAT')

_bot = telebot.TeleBot(TOKEN)
glossary = Glossary(Reducers.create)

start_msg = 'Доступні команди:\n/en\n' \
            'Але ми працюємо над покращенням :)'


def api_err_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApiException as e:
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
    text = message.text[3:]
    if not text:
        __send_msg(message.chat.id,
                   'Для пошуку англійських слів відправ повідомлення типу\n'
                   '<code>/en first, second, third</code>\n'
                   'Вони обов\'язково мають бути розділені комою з пробілом',
                   parse_mode='html', disable_web_page_preview=True)
    else:
        send_dict(message, text, 'Пошук англійських слів')


@_bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    __send_info(message)
    __send_msg(message.chat.id, start_msg, parse_mode='html')


@api_err_wrapper
def send_dict(message, words_str, first_msg):
    cid = message.chat.id

    def normalize(worrd):
        return worrd.strip(' ,.:\n').capitalize()

    words_arr = sorted(map(normalize, words_str.split(', ')))

    __send_msg(cid, first_msg, disable_web_page_preview=True)
    __send_msg(cid, f'Отримано слів: {len(words_arr)}')
    _bot.send_chat_action(cid, 'typing')

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
            __send_msg(cid, res, parse_mode='html')
            _bot.send_chat_action(cid, 'typing')
            res = ''

    __send_msg(cid, res, parse_mode='html')
    __send_msg(cid, start_msg)


class BotConfig:
    @staticmethod
    def process_updates(req):
        _bot.process_new_updates([telebot.types.Update.de_json(req)])

    @staticmethod
    def set_webhook(url):
        _bot.remove_webhook()
        _bot.set_webhook(url=url)
