import logging

from telegram import Update
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext

from app import dice


def bot_help(update: Update, context: CallbackContext):
    _args = context.args
    update.message.reply_text('Help!')


def weather(update: Update, context: CallbackContext):
    _args = context.args
    update.message.reply_text('weather!')


def tarot(update: Update, context: CallbackContext):
    _args = context.args
    update.message.reply_text('tarot!')


def fortune(update: Update, context: CallbackContext):
    _args = context.args
    reply = dice.fortune(None, None)
    update.message.reply_text(reply)


def make_reply(update: Update, context: CallbackContext):
    _args = context.args
    text = update.message.text
    if 'ㄆㄆ' in text:
        reply = '我知道！戳！'
        logging.info(f'reply: {reply}')
        update.message.reply_text(reply)
    elif '我看了' in text:
        update.message.reply_sticker(
            sticker='CAACAgUAAxkBAAMrXlNbUucnbiBebclIoM_qSMb52-sAAjoBAALvY54jySoLvI3DgmEYBA',
            reply_to_message_id=update.message.message_id,
            disable_notification=True,
        )


def add_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("help", bot_help, pass_args=True))
    dispatcher.add_handler(CommandHandler("weather", weather, pass_args=True))
    dispatcher.add_handler(CommandHandler("tarot", tarot, pass_args=True))
    dispatcher.add_handler(CommandHandler("fortune", fortune, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.text, make_reply, pass_args=True))
