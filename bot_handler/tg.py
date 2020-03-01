import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext

from app import dice
from app.ext_apis.util import reverse_geocode_customize


def bot_help(update: Update, _context: CallbackContext):
    # _args = context.args
    update.message.reply_text('Help!')


# from Code snippets
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#requesting-location-and-contact-from-user
def set_location(update: Update, _context: CallbackContext):
    # Requesting location and contact from user
    location_keyboard = KeyboardButton(text="我要提供位置資訊", request_location=True)
    contact_keyboard = KeyboardButton(text="我要提供電話資訊", request_contact=True)
    custom_keyboard = [[location_keyboard, contact_keyboard]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
        text="你想提供什麼資訊讓朽咪提供更多服務呢？\n位置資訊會用來提供天氣服務，電話號碼目前沒有作用。",
        reply_markup=reply_markup
    )


def weather(update: Update, _context: CallbackContext):
    # _args = context.args
    logger = logging.getLogger(__name__)
    location = update.message.location
    if not location:
        update.message.reply_text('朽咪不知道您的位置資訊，所以無法提供天氣服務，請使用 /set_location 指令提供位置資訊')
    else:
        lat = location.latitude
        lon = location.longitude
        geo_info = reverse_geocode_customize((lat, lon))[0]
        update.message.reply_text(f'您的位置資訊：{geo_info["name"]}, {geo_info["admin1"]}, {geo_info["cc"]} ({lat}, {lon})')


def tarot(update: Update, _context: CallbackContext):
    # _args = context.args
    card = dice.draw_tarot()
    update.message.reply_photo(
        photo=card['url'],
        caption=card['nameCN'],
        disable_notification=True,
        reply_to_message_id=update.message.message_id,
    )


def fortune(update: Update, _context: CallbackContext):
    # _args = context.args
    reply = dice.fortune(None, None)
    update.message.reply_text(reply)


def make_reply(update: Update, _context: CallbackContext):
    # _args = context.args
    text = update.message.text
    logger = logging.getLogger(__name__)
    if 'ㄆㄆ' in text:
        reply = '我知道！戳！'
        logger.info(f'reply: {reply}')
        update.message.reply_text(reply)
    elif '我看了' in text:
        update.message.reply_sticker(
            sticker='CAACAgUAAxkBAAMrXlNbUucnbiBebclIoM_qSMb52-sAAjoBAALvY54jySoLvI3DgmEYBA',
            disable_notification=True,
            reply_to_message_id=update.message.message_id,
        )


def add_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("help", bot_help, pass_args=True))
    dispatcher.add_handler(CommandHandler("setlocation", set_location, pass_args=True))
    dispatcher.add_handler(CommandHandler("weather", weather, pass_args=True))
    dispatcher.add_handler(CommandHandler("tarot", tarot, pass_args=True))
    dispatcher.add_handler(CommandHandler("fortune", fortune, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.text, make_reply))
