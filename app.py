from flask import Flask, request

from modules.bot import BotConfig

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

token = os.getenv('TELEGRAM_TOKEN')
webhook_url = os.getenv('WEBHOOK')
port = os.getenv('PORT')


@app.route('/' + token, methods=['POST'])
def getMessage():
    BotConfig.process_updates(request.stream.read().decode("utf-8"))
    return "!", 200


@app.route("/")
def set_webhook():
    BotConfig.set_webhook(webhook_url + '/' + token)
    return "!", 200


if __name__ == "__main__":
    app.run()
