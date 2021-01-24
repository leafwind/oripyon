"""
Interface of LikeCoin Telegram bot
"""
import logging
from typing import Dict, Tuple, List

import requests
from cachetools import cached, TTLCache
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext, CallbackQueryHandler

reply_rabbit_icon = "\U0001F430"
validator_icon = "\U0001F47E"


# cache validator status for no longer than 1hour
@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_validators():
    r = requests.get("https://mainnet-node.like.co/staking/validators")
    return r.json()["result"]


# cache validator voting power for no longer than 1hour
@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_validators_voting_power() -> Tuple[Dict, float]:
    r = requests.get("https://mainnet-node.like.co/validatorsets/latest")
    validators_power = r.json()["result"]["validators"]
    voting_power_map = {}
    voting_power_total = 0.0
    for v in validators_power:
        voting_power = float(v["voting_power"])
        voting_power_map[v["address"]] = voting_power
        voting_power_total += voting_power
    return voting_power_map, voting_power_total


# cache validator status for no longer than 1hour
@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_inflation() -> float:
    r = requests.get("https://mainnet-node.like.co/minting/inflation")
    return float(r.json()["result"])


# cache validator status for no longer than 1hour
@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_staking_pool() -> float:
    r = requests.get("https://mainnet-node.like.co/staking/pool")
    nano_like = float(r.json()["result"]["bonded_tokens"])
    return nano_like / 1000000000


# cache validator status for no longer than 1hour
@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_supply() -> float:
    r = requests.get("https://mainnet-node.like.co/supply/total")
    nano_like = float(r.json()["result"][0]["amount"])
    return nano_like / 1000000000


# cache all proposal status for no longer than 1hour
@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_proposals() -> Tuple[List[str], List[str]]:
    r = requests.get("https://mainnet-node.like.co/gov/proposals")
    result = r.json()["result"]
    existing_proposal_id = []
    ongoing_proposal_id = []
    for proposal in result:
        existing_proposal_id.append(proposal["id"])
        if proposal["proposal_status"] == "VotingPeriod":
            ongoing_proposal_id.append(proposal["id"])
    return existing_proposal_id, ongoing_proposal_id


# cache single proposal status for no longer than 1hour
@cached(cache=TTLCache(maxsize=256, ttl=3600))
def get_proposal(proposal_id: str) -> Dict:
    r = requests.get(f"https://mainnet-node.like.co/gov/proposals/{proposal_id}/votes")
    vote_record_map = {}
    for vote in r.json()["result"]:
        vote_record_map[vote["voter"]] = vote["option"]
    return vote_record_map


# cache participated proposals for each validators
@cached(cache=TTLCache(maxsize=256, ttl=3600))
def get_participated_proposal(validator_address: str) -> Tuple[int, int]:
    existing_proposal_id, _ongoing_proposal_id = get_proposals()
    participated = 0
    for proposal_id in existing_proposal_id:
        if validator_address in get_proposal(proposal_id):
            participated += 1
    return participated, len(existing_proposal_id)


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


def get_inline_validators_button_markup():
    validator_buttons = [
        InlineKeyboardButton(
            text=v['description']['moniker'],
            callback_data=f"{validator_icon} {v['operator_address']}"
        )
        for v in get_validators()
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
    return markup


def validator_status(update: Update, _context: CallbackContext):
    markup = get_inline_validators_button_markup()
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
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Otherwise, the edit_message_text() function will create a new message
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data.startswith(validator_icon):
        validator_address = query.data.split()[1]
        logging.info(f"validator_address: {validator_address}")
        for v in get_validators():
            if validator_address == v['operator_address']:
                logging.info(f"found: {v['description']['moniker']}")
                commission_rate = v["commission"]["commission_rates"]["rate"]
                apr = get_inflation() / (get_staking_pool() / get_supply()) * (1 - float(commission_rate))
                voting_power_map, voting_power_total = get_validators_voting_power()
                _existing_proposal_id, ongoing_proposal_id = get_proposals()
                num_participated_proposal, num_total_proposal = get_participated_proposal(validator_address)
                ongoing_proposal_activities = [f"    議案 {proposal_id}: {get_proposal(proposal_id).get(validator_address, '未表態')}\n" for proposal_id in ongoing_proposal_id]
                text = f"validator: {v['description']['moniker']}\n" \
                    f"投票權排名: {voting_power_map['validator_address'] / voting_power_total:.2%}\n" \
                    f"佣金: {float(commission_rate):.0%}\n" \
                    f"預估年收益: {apr:.2%}\n" \
                    f"參與度（投票議案／有效議案）: {num_participated_proposal} / {num_total_proposal}\n" \
                    f"進行中的議案表態: \n{ongoing_proposal_activities}"
                query.edit_message_text(
                    text=f"請選擇要查詢的驗證人 {reply_rabbit_icon}\n" + wrap_code_block(text),
                    parse_mode="MarkdownV2",
                    reply_markup=get_inline_validators_button_markup()
                )
                return
        logging.info(f"cannot find {validator_address}")
        text = f"validator: {validator_address} not found\n"
        query.edit_message_text(
            text=f"請選擇要查詢的驗證人 {reply_rabbit_icon}\n" + wrap_code_block(text),
            parse_mode="MarkdownV2",
            reply_markup=get_inline_validators_button_markup()
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
