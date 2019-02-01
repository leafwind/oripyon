# -*- coding: utf-8 -*-

import logging
import re
import os
import random

from linebot.models import (
    TextSendMessage, ImageSendMessage
)
from app.phrase import horse_phrase, lion_phrase, dunkey_phrase
maple_phrase = horse_phrase + lion_phrase + dunkey_phrase

GROUP_IDS = {
    'test': 'C1bebaeaf89242089f0d755d492df6cb6',
    'luna': 'C690e08d2fb900d5bbd873e103d500b92',
    'yebai': 'C25add4301bc790a641e07b02b868a9b7',
    'maplestory': 'C0cd56d37156c5ad3fe04b702624d50dd',
    'lineage_m': 'C2f63f279abd655966368630816bd0cad',
    'mao_sino_alice': 'Cfb6a76351d112834244144a1cd4f0f57',
    'nier_sino_alice': 'C1e38a92f8c7b4ad377df882b9f3bf336',
}

help_find_pattern = re.compile('協尋'.decode('utf-8'))


def group_reply_test(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['test']:
        return
    logging.info('頻道：%s', '測試群組')
    if msg == '!hinet':
        image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/BFTQEnG.png',
            preview_image_url='https://i.imgur.com/BFTQEnG.png',
        )
        line_bot_api.reply_message(reply_token, [image_message])
    return


def group_reply_lineage_m(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['lineage_m']:
        return
    logging.info('頻道：%s', '天堂老司機')
    return


def group_reply_maplestory(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['maplestory']:
        return
    logging.info('頻道：%s', '小路北七群')
    if '小路占卜'.decode('utf-8') in msg:
        global maple_phrase
        random.seed(os.urandom(5))
        ph = random.choice(maple_phrase)
        msg = '今日運勢：{}'.decode('utf-8').format(ph.decode('utf-8'))
    else:
        return None
    line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=msg)
        ])
    return


def group_reply_yebai(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['yebai']:
        return
    logging.info('頻道：%s', '葉白')
    if help_find_pattern.search(msg):
        image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/ksIHMn6.jpg',
            preview_image_url='https://i.imgur.com/ksIHMn6.jpg',
        )
        line_bot_api.reply_message(reply_token, [
            image_message,
            TextSendMessage(text=u'請幫幫忙找找他...等等他是誰？(((ﾟДﾟ;)))'.encode('utf-8'))
        ])
    return


def group_reply_mao_sino_alice(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['mao_sino_alice']:
        return
    logging.info('頻道：%s', '死愛魔王城')
    if '測試'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'@FuryNerd'.encode('utf-8'))
        ])
        return


def group_reply_nier_sino_alice(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['mao_sino_alice']:
        return
    logging.info('頻道：%s', '尼爾主題餐廳')
    if '頓頓是我的'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'是我的！！'.encode('utf-8'))
        ])
        return
    elif '名字是我的'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'是我的！！'.encode('utf-8'))
        ])
        return


def group_reply_luna(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['luna']:
        return
    logging.info('頻道：%s', '皇家御貓園')
    if '涼哥是怎樣的人'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'正直善良又誠懇、不會說話卻實在'.encode('utf-8'))
        ])
        return
    return
