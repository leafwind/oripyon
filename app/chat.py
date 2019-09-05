import logging
import os
import random

import Levenshtein
from linebot.models import TextSendMessage

from app.emoji_list import KAOMOJI_LIST
from app.markov_chain import MarkovChat
from constants import TEST_GROUP_IDS

markov_chat_instance_map = {}


def chat(line_bot_api, reply_token, source_id, msg, log_filename):
    global markov_chat_instance_map
    if source_id not in markov_chat_instance_map:
        # new MarkovChat obj
        mc = MarkovChat(os.path.join('./training', log_filename), chattiness=1)
        markov_chat_instance_map[source_id] = mc
    else:
        # reuse MarkovChat obj to save memory
        mc = markov_chat_instance_map[source_id]
    log = mc.log(msg)
    if log:
        log_similarity = Levenshtein.ratio(msg, log)
        logging.info('log: %s (sim: %s)', log, log_similarity)
        if source_id in TEST_GROUP_IDS:
            random.seed(os.urandom(5))
            line_bot_api.reply_message(reply_token, [TextSendMessage(text=random.choice(KAOMOJI_LIST) + log)])

    chat = mc.chat(msg)
    if chat:
        chat_similarity = Levenshtein.ratio(msg, chat)
        logging.info('chat: %s (sim: %s)', chat, chat_similarity)
