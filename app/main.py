import logging
import ssl
import sys

import telegram
import yaml
from flask import Flask, request, abort, render_template
from linebot import WebhookHandler
from linebot.exceptions import (
    InvalidSignatureError
)
from telegram.ext import Dispatcher

from app.sqlite_utils.user_location import check_or_create_table_tg_user_location, insert_tg_user_location
from bot_handler import line, tg

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests.packages.urllib3").setLevel(logging.WARNING)
logging.getLogger("oauth2client").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)


def set_logger():
    log_level = logging.INFO
    my_format = "[%(levelname).4s] %(asctime)s | %(name)s | " \
                "%(lineno)3s | %(message)s"
    date_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(my_format, date_fmt)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(h)
    root_logger.setLevel(log_level)
    return


# logging config should before Flask app init
# if not, Flask will write to stderr by default
set_logger()

application = Flask(__name__, template_folder='templates')

with open("bot_token.yml", 'r') as stream:
    data = yaml.safe_load(stream)
    LINE_CHANNEL_SECRET = data['LINE_CHANNEL_SECRET']
    TELEGRAM_TOKEN = data['TELEGRAM_TOKEN']
line_web_hook_handler = WebhookHandler(LINE_CHANNEL_SECRET)
telegram_bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Context based callbacks
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Transition-guide-to-Version-12.0#context-based-callbacks
# If you do not use Updater but only Dispatcher you should instead set use_context=True when you create the Dispatcher.
dispatcher = Dispatcher(telegram_bot, None, use_context=True)

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
        logger = logging.getLogger(__name__)
        logger.debug('body: %s', body)
        line.add_event_handlers(line_web_hook_handler)
        line.add_message_handlers(line_web_hook_handler)
        line_web_hook_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# telegram callback endpoint
@application.route("/telegram_callback", methods=['POST'])
def telegram_callback():
    logger = logging.getLogger(__name__)
    tg.add_handlers(dispatcher)
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), telegram_bot)
        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
        logger.info(f'user_id: {update.effective_user.id}, message: {update.message.text}')
        if not update.message.text:
            logging.warning(f'no text attribute in: {update.message}')
        if update.message.sticker is not None:
            logger.info(f'sticker file_id: {update.message.sticker.file_id}')
        if update.message.location is not None:
            location = update.message.location
            lat = location.latitude
            lon = location.longitude
            user = update.effective_user
            update.message.reply_text(
                f'您的資訊將會被朽咪記住，天氣預測功能將根據以下這些資訊提供服務：\n'
                f'\U0001F194 {user.id}\n'
                f'\U00003294 first name: {user.first_name}\n'
                f'\U0001F464 username: {user.username}\n'
                f'\U0001F310 經緯度: {lat}, {lon}'
            )
            check_or_create_table_tg_user_location()
            insert_tg_user_location(user.id, user.first_name, user.username, lat, lon)
    return 'OK'


# dev web server for testing
if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(
        '/etc/ssl/private/letsencrypt-domain.pem',
        '/etc/ssl/private/letsencrypt-domain.key'
    )
    application.run(ssl_context=ssl_context, port=5000)
