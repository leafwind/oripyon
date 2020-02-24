import json
import logging


def parse_cmd_text(text):
    # Telegram understands UTF-8, so encode text for unicode compatibility
    # text = text.encode('utf-8')
    cmd = None
    if '/' in text:
        try:
            i = text.index(' ')
        except ValueError:
            return text, None
        cmd = text[:i]
        text = text[i + 1:]
    return cmd, text


def echo(telegram_bot, message):
    """
    repeat the same message back (echo)
    """
    chat_id = message.chat.id
    _cmd, text = parse_cmd_text(message.text)
    if text is None or len(text) == 0:
        pass
    else:
        reply = json.dumps(text, ensure_ascii=False)
        reply = reply.strip('\"')
        logging.info(f'reply: {reply}')
        telegram_bot.sendMessage(chat_id=chat_id, text=reply)


def handle_message(telegram_bot, message):
    chat_id = message.chat.id
    logging.info(f'chat_id: {chat_id}, text: {message.text}')
    if message.text is None:
        return
    text = message.text
    if '/echo' in text:
        echo(telegram_bot, message)
    elif 'ㄆㄆ' in text:
        reply = '我知道！戳！'
        logging.info(f'reply: {reply}')
        telegram_bot.sendMessage(chat_id=chat_id, text=reply)
    elif '我看了' in text:
        telegram_bot.send_sticker(
            chat_id=chat_id,
            sticker='CAACAgUAAxkBAAMrXlNbUucnbiBebclIoM_qSMb52-sAAjoBAALvY54jySoLvI3DgmEYBA',
            reply_to_message_id=message.message_id,
            disable_notification=True,
        )
    else:
        pass
