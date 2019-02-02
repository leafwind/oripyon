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
    'test': {
        'name': '測試群組',
        'id': 'C1bebaeaf89242089f0d755d492df6cb6',
    },
    'luna': {
        'name': '皇家御貓園',
        'id': 'C690e08d2fb900d5bbd873e103d500b92',
    },
    'yebai': {
        'name': '葉白',
        'id': 'C25add4301bc790a641e07b02b868a9b7',
    },
    'maplestory': {
        'name': '小路北七群',
        'id': 'C0cd56d37156c5ad3fe04b702624d50dd',
    },
    'lineage_m': {
        'name': '天堂老司機',
        'id': 'C2f63f279abd655966368630816bd0cad',
    },
    'mao_sino_alice': {
        'name': '死愛魔王城',
        'id': 'Cfb6a76351d112834244144a1cd4f0f57',
    },
    'nier_sino_alice': {
        'name': '尼爾主題餐廳',
        'id': 'C1e38a92f8c7b4ad377df882b9f3bf336',
    },
}

GROUP_ID_NANE = {}
for key in GROUP_IDS:
    GROUP_ID_NANE[GROUP_IDS[key]['id']] = GROUP_IDS[key]['name']

help_find_pattern = re.compile('協尋'.decode('utf-8'))


def group_reply_test(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['test']['id']:
        return
    if msg == '!hinet':
        image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/BFTQEnG.png',
            preview_image_url='https://i.imgur.com/BFTQEnG.png',
        )
        line_bot_api.reply_message(reply_token, [image_message])
    return


def group_reply_lineage_m(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['lineage_m']['id']:
        return
    return


def group_reply_maplestory(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['maplestory']['id']:
        return
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
    if source_id != GROUP_IDS['yebai']['id']:
        return
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
    if source_id != GROUP_IDS['mao_sino_alice']['id']:
        return
    if '小米米'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'綁起來電擊烤焦爆香切段上菜（¯﹃¯）'.encode('utf-8'))
        ])
        return
    elif '2050'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'兩洞伍洞，部隊起床｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡'.encode('utf-8')),
            TextSendMessage(text=u'睡你麻痺起來嗨ヽ(`Д´)ノ'.encode('utf-8')),
        ])
        return
    elif '死愛資料庫'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'https://sinoalice.game-db.tw/'.encode('utf-8')),
        ])
        return


def group_reply_nier_sino_alice(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['nier_sino_alice']['id']:
        return
    if '頓頓是我的'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'是我的！！'.encode('utf-8'))
        ])
        return
    elif '名字' in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'是我的！！'.encode('utf-8'))
        ])
        return
    elif '雞排是我的'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'是我的！！'.encode('utf-8'))
        ])
        return
    elif '生哥是我的'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'好阿給你。'.encode('utf-8'))
        ])
        return
    elif '死愛資料庫'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'https://sinoalice.game-db.tw/'.encode('utf-8')),
        ])
        return


def group_reply_luna(msg, line_bot_api, source_id, reply_token):
    if source_id != GROUP_IDS['luna']['id']:
        return
    if '涼哥是怎樣的人'.decode('utf-8') in msg:
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=u'正直善良又誠懇、不會說話卻實在'.encode('utf-8'))
        ])
        return
    return
