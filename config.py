DEVELOP = False
WEBHOOK_URL = ''
TELEGRAM_TOKEN = ''  # @auto_glossary_bot

try:
    from local import *
except ImportError:
    pass
