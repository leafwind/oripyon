import json
import logging


def parse_cmd_text(text):
    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = text.encode('utf-8')
    cmd = None
    if b'/' in text:
        try:
            i = text.index(b' ')
        except ValueError:
            return text, None
        cmd = text[:i]
        text = text[i + 1:]
    return cmd, text


def echo(telegram_bot, message):
    """
    repeat the same message back (echo)
    """
    _cmd, text = parse_cmd_text(message.text)
    if text is None or len(text) == 0:
        pass
    else:
        logging.info(f'message.chat.id: {message.chat.id}, text: {text.decode("utf-8")}')
        chat_id = message.chat.id
        reply = json.dumps(text.decode('utf-8'), ensure_ascii=False).encode('utf-8')
        logging.info(f'reply: {reply}')
        telegram_bot.sendMessage(chat_id=chat_id, text=reply)


def handle_message(telegram_bot, message):
    if message.text is None:
        return
    text = message.text
    if '/echo' in text:
        echo(telegram_bot, message)
