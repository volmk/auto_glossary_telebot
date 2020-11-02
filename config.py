DEVELOP = False
WEBHOOK_URL = 'https://tranquil-bayou-74967.herokuapp.com'
TELEGRAM_TOKEN = '1301995094:AAHzkaJ9-iaTyj2Zgx_lUmHDpXXaVb2vyWY'  # @auto_glossary_bot

try:
    from local import *
except ImportError:
    pass
