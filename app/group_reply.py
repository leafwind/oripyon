# -*- coding: utf-8 -*-

import logging
import re

from linebot.models import (
    TextSendMessage, ImageSendMessage
)

GROUP_IDS = {
    'test': 'C1bebaeaf89242089f0d755d492df6cb6',
    'luna': 'C690e08d2fb900d5bbd873e103d500b92',
    'yebai': 'C25add4301bc790a641e07b02b868a9b7',
    'maplestory': 'C0cd56d37156c5ad3fe04b702624d50dd',
    'lineage_m': 'C2f63f279abd655966368630816bd0cad',
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
        line_bot_api.reply_message(reply_token, [ image_message ])
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
    return

def group_reply_yebai(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['yebai']:
        return
    logging.info('頻道：%s', '葉白')
    if help_find_pattern.search(msg):
        image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/igrFN9F.jpg',
            preview_image_url='https://i.imgur.com/igrFN9F.jpg',
        )
        line_bot_api.reply_message(reply_token, [
            image_message,
            TextSendMessage(text=u'請幫幫忙找找他...等等他是誰？(((ﾟДﾟ;)))'.encode('utf-8'))
        ])
    return

def group_reply_luna(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['luna']:
        return
    logging.info('頻道：%s', '皇家御貓園')
    if '涼哥是怎樣的人'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            image_message,
            TextSendMessage(text=u'正直善良又誠懇、不會說話卻實在'.encode('utf-8'))
        ])
        return
    return
