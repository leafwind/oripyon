"""
Interface of LikeCoin Telegram bot
"""
import logging

import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext

reply_rabbit_icon = "\U0001F430"
validator_icon = "\U0001F471"


def get_function_keyboard_markup(chat_type):
    proposal_status_button = KeyboardButton(text='\U0001F5F3 現有議案')
    validator_status_button = KeyboardButton(text=f"{validator_icon} 驗證人狀態")
    feedback_button = KeyboardButton(text='\U0001F465 建議交流')
    close_button = KeyboardButton(text='\U0000274E 關閉鍵盤')
    custom_keyboard = [
        [proposal_status_button, validator_status_button],
        [feedback_button, close_button],
    ]
    markup = ReplyKeyboardMarkup(
        custom_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True,
    )
    return markup


def proposal_status(update: Update, _context: CallbackContext):
    update.message.reply_text("TODO")


def validator_status(update: Update, _context: CallbackContext):
    r = requests.get("https://mainnet-node.like.co/staking/validators")
    result = r.json()
    validators = result["result"]
    validator_buttons = [
        KeyboardButton(text=f"{validator_icon} {v['description']['moniker']}")
        for v in validators
    ]
    custom_keyboard = [
        validator_buttons,
        [KeyboardButton(text='\U0000274E 關閉鍵盤')]
    ]
    markup = ReplyKeyboardMarkup(
        custom_keyboard,
        resize_keyboard=True,
        selective=True,
    )

    reply = f"請選擇要查詢的驗證人 {reply_rabbit_icon}"
    update.message.reply_text(
        text=reply,
        reply_markup=markup
    )


def feedback(update: Update, _context: CallbackContext):
    reply = f'聯絡作者 @leafwind_tw\n' \
            f'加入 LikeCoin Discord 伺服器一起討論 https://discord.com/invite/W4DQ6peZZZ'
    update.message.reply_text(reply)


def close_keyboard(update: Update, _context: CallbackContext):
    reply = f"OK! {reply_rabbit_icon}"
    logging.getLogger(__name__).info(f'reply: {reply}')
    update.message.reply_text(reply, reply_markup=ReplyKeyboardRemove())


def make_reply(update: Update, _context: CallbackContext):
    # _args = context.args
    if not update.message.text:
        logging.warning(f'no text attribute in: {update.message}')
    text = update.message.text
    logger = logging.getLogger(__name__)
    if text == "\U0001F5F3 現有議案":
        proposal_status(update, _context)
    elif text == f"{validator_icon} 驗證人狀態":
        validator_status(update, _context)
    elif text == "\U0001F465 建議交流":
        feedback(update, _context)
    elif text == "\U0000274E 關閉鍵盤":
        close_keyboard(update, _context)
    elif "沒事了" in text:
        reply = f"沒事就好 {reply_rabbit_icon}"
        logger.info(f"reply: {reply}")
        update.message.reply_text(reply)


def bot_help(update: Update, _context: CallbackContext):
    # _args = context.args
    update.message.reply_text(
        text=f'你可以：\n'
             f'輸入 "/" 展開指令選單\n'
             f'使用貼圖旁邊的 [ / ] 按鈕展開指令選單\n'
             f'使用下面的鍵盤選單',
        reply_markup=get_function_keyboard_markup(update.message.chat.type)
    )


def add_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("help", bot_help, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.text, make_reply))
