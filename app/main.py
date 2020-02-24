import logging
import ssl

import telegram
import yaml
from flask import Flask, request, abort, render_template
from linebot import WebhookHandler
from linebot.exceptions import (
    InvalidSignatureError
)

from bot_handler.line_handler import add_handlers
from bot_handler.telegram_handler import handle_message

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests.packages.urllib3").setLevel(logging.WARNING)
logging.getLogger("oauth2client").setLevel(logging.WARNING)
application = Flask(__name__, template_folder='templates')


with open("line_auth_key.yml", 'r') as stream:
    data = yaml.safe_load(stream)
    CHANNEL_SECRET = data['CHANNEL_SECRET']
line_web_hook_handler = WebhookHandler(CHANNEL_SECRET)

with open("telegram_token.yml", 'r') as stream:
    data = yaml.safe_load(stream)
    TELEGRAM_TOKEN = data['TELEGRAM_TOKEN']
telegram_bot = telegram.Bot(token=TELEGRAM_TOKEN)


# index endpoint
@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# line callback endpoint
@application.route("/line_callback", methods=['POST'])
def line_callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle Web hook body
    try:
        # logging.info('body: %s', body)
        add_handlers(line_web_hook_handler)
        line_web_hook_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# telegram callback endpoint
@application.route("/telegram_callback", methods=['POST'])
def telegram_callback():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), telegram_bot)
        # logging.info(update.message.sticker.__dict__)
        handle_message(telegram_bot, update.message)
    return 'OK'


# dev web server for testing
if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(
        '/etc/ssl/private/letsencrypt-domain.pem',
        '/etc/ssl/private/letsencrypt-domain.key'
    )
    application.run(ssl_context=ssl_context, port=5000)
