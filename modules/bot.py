from config import TELEGRAM_TOKEN
import telebot

from modules.glossary import Glossary
from modules.reducers import Reducers

_bot = telebot.TeleBot(TELEGRAM_TOKEN)

start_message = 'Відправ слова. Вони мають бути розділені комою з пробілом. Слова сортуються автоматично\n' \
                'Доступні команди:\n/start\n/camb\n/dict\n' \
                'Для пошуку на обох сайтах просто відправ слова'


@_bot.message_handler(commands=['start'])
def start(message):
    _bot.send_message(message.chat.id, start_message, parse_mode='html', disable_web_page_preview=True)


@_bot.message_handler(commands=['camb'])
def camb(message):
    text = message.text[5:]
    if not text:
        _bot.send_message(message.chat.id, 'Відправ повідомлення типу <code>'
                                           '\n/camb first, second, third\n'
                                           '</code> для пошуку на сайті https://dictionary.cambridge.org/',
                          parse_mode='html', disable_web_page_preview=True)
    else:
        send_dict(message, text, Reducers.dictionary_cambridge_org, 'Пошук на сайті https://dictionary.cambridge.org/')


@_bot.message_handler(commands=['dict'])
def dict(message):
    text = message.text[5:]
    if not text:
        _bot.send_message(message.chat.id, 'Відправ повідомлення типу <code>'
                                           '\n/dict first, second, third\n'
                                           '</code> для пошуку на сайті https://www.dictionary.com/',
                          parse_mode='html', disable_web_page_preview=True)
    else:
        send_dict(message, text, Reducers.dictionary_com, 'Пошук на сайті https://dictionary.com/')


@_bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    send_dict(message, message.text, Reducers.default,
              'Пошук на сайтах https://dictionary.cambridge.org/ та https://dictionary.com/')


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
    _bot.send_message(cid, start_message)


class BotConfig:
    @staticmethod
    def process_updates(req):
        _bot.process_new_updates([telebot.types.Update.de_json(req)])

    @staticmethod
    def set_webhook(url):
        _bot.remove_webhook()
        _bot.set_webhook(url=url)
