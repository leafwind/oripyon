"""
Interface of LikeCoin Telegram bot
"""
import logging

import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext, CallbackQueryHandler

reply_rabbit_icon = "\U0001F430"
validator_icon = "\U0001F47E"
validators = []


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


def get_single_validator_status(update: Update, _context: CallbackContext):
    return


def proposal_status(update: Update, _context: CallbackContext):
    update.message.reply_text("TODO")


def validator_status(update: Update, _context: CallbackContext):
    global validators
    r = requests.get("https://mainnet-node.like.co/staking/validators")
    result = r.json()
    validators = result["result"]
    validator_buttons = [
        InlineKeyboardButton(
            text=v['description']['moniker'],
            callback_data=f"{validator_icon} {v['operator_address']}"
        )
        for v in validators
    ]
    validator_table = []
    # re-format 1-D button list to 2-D button list of list
    num_of_col = 3
    while validator_buttons:
        row = []
        for i in range(num_of_col):
            row.append(validator_buttons.pop(0))
        validator_table.append(row)
    markup = InlineKeyboardMarkup(validator_table)

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


def text_reply_handler(update: Update, _context: CallbackContext):
    # _args = context.args
    if not update.message.text:
        logging.warning(f'no text attribute in: {update.message}')
    text = update.message.text
    if text == "\U0001F5F3 現有議案":
        proposal_status(update, _context)
    elif text == f"{validator_icon} 驗證人狀態":
        validator_status(update, _context)
    elif text == "\U0001F465 建議交流":
        feedback(update, _context)
    elif text == "\U0000274E 關閉鍵盤":
        close_keyboard(update, _context)
    elif text.startswith(f"{validator_icon} "):
        get_single_validator_status(update, _context)


def wrap_code_block(text: str) -> str:
    return "```\n" + text + "```"


def callback_query_handler(update: Update, _context: CallbackContext):
    cqd = update.callback_query.data
    if cqd.startswith(validator_icon):
        validator_address = cqd.split()[1]
        logging.info(f"validator_address: {validator_address}")
        for v in validators:
            if validator_address == v['operator_address']:
                logging.info(f"found: {v['description']['moniker']}")
                commission_rate = v["commission"]["commission_rates"]["rate"]
                text = f"validator: {v['description']['moniker']}\n" \
                    f"commission rate: {float(commission_rate):.0%}\n"
                update.callback_query.edit_message_text(
                    text=f"請選擇要查詢的驗證人 {reply_rabbit_icon}\n" + wrap_code_block(text),
                    parse_mode="MarkdownV2",
                )
                return
        logging.info(f"cannot find {validator_address}")
        text = f"validator: {validator_address} not found\n"
        update.callback_query.edit_message_text(
            text=f"請選擇要查詢的驗證人 {reply_rabbit_icon}\n" + wrap_code_block(text),
            parse_mode="MarkdownV2",
        )
        return


def start_handler(update: Update, _context: CallbackContext):
    update.message.reply_text(
        text=f'你可以：\n'
             f'輸入 "/" 展開指令選單\n'
             f'使用貼圖旁邊的 [ / ] 按鈕展開指令選單\n'
             f'使用下面的鍵盤選單',
        reply_markup=get_function_keyboard_markup(update.message.chat.type)
    )


def add_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, text_reply_handler))
    dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
