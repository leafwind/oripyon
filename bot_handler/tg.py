import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext

from app import dice
from app.ext_apis.util import reverse_geocode_customize
from app.sqlite_utils.user_location import query_tg_user_location


def bot_help(update: Update, _context: CallbackContext):
    # _args = context.args
    update.message.reply_text('Help!')


def get_location_keyboard_markup():
    location_keyboard = KeyboardButton(text="我要提供位置資訊", request_location=True)
    reject_keyboard = KeyboardButton(text="先不要")
    custom_keyboard = [[location_keyboard, reject_keyboard]]
    markup = ReplyKeyboardMarkup(
        custom_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup


# from Code snippets
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#requesting-location-and-contact-from-user
def set_location(update: Update, _context: CallbackContext):
    update.message.reply_text(
        text="你想提供位置資訊讓朽咪提供更多服務嗎？",
        reply_markup=get_location_keyboard_markup()
    )


def weather(update: Update, _context: CallbackContext):
    # _args = context.args
    gps_location = query_tg_user_location(update.effective_user.user_id)
    lat, lon = gps_location
    if not gps_location:
        update.message.reply_text(
            text='朽咪不知道您的位置資訊，你想提供位置資訊讓朽咪提供更多服務嗎？',
            reply_markup=get_location_keyboard_markup()
        )
    else:
        geo_info = reverse_geocode_customize((lat, lon))[0]
        update.message.reply_text(
            f'地名: {geo_info["name"]}\n'
            f'一級行政區: {geo_info["admin1"]}\n'
            f'國家: {geo_info["cc"]}'
        )


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
    elif '沒事了' in text:
        reply = '沒事就好\U0001F430'
        logger.info(f'reply: {reply}')
        update.message.reply_text(reply)


def add_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("help", bot_help, pass_args=True))
    dispatcher.add_handler(CommandHandler("setlocation", set_location, pass_args=True))
    dispatcher.add_handler(CommandHandler("weather", weather, pass_args=True))
    dispatcher.add_handler(CommandHandler("tarot", tarot, pass_args=True))
    dispatcher.add_handler(CommandHandler("fortune", fortune, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.text, make_reply))
