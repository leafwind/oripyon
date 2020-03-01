import logging

from telegram import Update
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext

from app import dice


def bot_help(update: Update, _context: CallbackContext):
    # _args = context.args
    update.message.reply_text('Help!')


def weather(update: Update, _context: CallbackContext):
    # _args = context.args
    update.message.reply_text('weather!')


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
    logger.info(f'location: {update.message.location}')
    # lat = update.message.location.latitude
    # lon = update.message.location.longitude
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
    dispatcher.add_handler(CommandHandler("weather", weather, pass_args=True))
    dispatcher.add_handler(CommandHandler("tarot", tarot, pass_args=True))
    dispatcher.add_handler(CommandHandler("fortune", fortune, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.text, make_reply))
