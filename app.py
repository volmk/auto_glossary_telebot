from flask import Flask, request

from modules.bot import BotConfig

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
DEV_MODE = os.getenv('DEV_MODE')


@app.route('/' + TOKEN, methods=['POST'])
def botmsg():
    BotConfig.process_updates(request.stream.read().decode("utf-8"))
    return "!", 200


@app.route("/wakeup")
def wakeup():
    return "!", 200


@app.route("/sethook")
def sethook():
    BotConfig.set_webhook(WEBHOOK_URL + '/' + TOKEN)
    return "changed", 200


if __name__ == "__main__":
    app.run()
