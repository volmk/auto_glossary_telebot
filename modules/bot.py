from config import TELEGRAM_TOKEN
import telebot

from modules.glossary import Glossary
from modules.reducers import Reducers

_bot = telebot.TeleBot(TELEGRAM_TOKEN)

start_message = 'Відправ слова. Вони мають бути розділені комою з пробілом'

@_bot.message_handler(commands=['start'])
def start(message):
    _bot.send_message(message.chat.id, start_message, parse_mode='html')


@_bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    cid = message.chat.id
    words_arr = sorted(map(str.capitalize, message.text.split(', ')))

    _bot.send_message(cid, f'Отримано слів: {len(words_arr)}')
    _bot.send_chat_action(cid, 'typing')

    glossary = Glossary(Reducers.dictionary_com)
    res = ''

    for idx, s in enumerate(words_arr, 1):
        word = s.translate({' ': '%20'})
        res += glossary.create_html(word, idx)

        if idx % 20 == 0 or len(res) > 3500:
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

