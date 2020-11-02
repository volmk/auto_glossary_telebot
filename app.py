from flask import Flask, request

from config import WEBHOOK_URL, TELEGRAM_TOKEN

from modules.bot import BotConfig

app = Flask(__name__)


@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def getMessage():
    BotConfig.process_updates(request.stream.read().decode("utf-8"))
    return "!", 200


@app.route("/")
def webhook():
    BotConfig.set_webhook(WEBHOOK_URL + '/' + TELEGRAM_TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run()
