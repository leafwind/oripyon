# -*- coding: utf-8 -*-
import os
import random
from app.config import CHANNEL_SECRET, CHANNEL_ACCESS_TOKEN
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from app.phrase import horse_phrase, lion_phrase, dunkey_phrase
maple_phrase = horse_phrase + lion_phrase + dunkey_phrase

wtf_reason = [
    '一例一休',
    '陸客不來了',
    '一個阿嬤嘎挖共，不出來選，天公伯不會原諒我',
    '只要是男人就會喜歡邱主任',
    '車子她開的～我上了她的車～就～咻的滑進摩鐵了',
]

application = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@application.route('/')
def hello_world():
    return 'Hello World from flaskapp2!'

@application.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    application.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('=========')
    print(event.__dict__)
    print(event.source.__dict__)
    if event.source.type == 'room':
        rid = event.source.room_id
        reply = make_reply('room', rid, event.message.text)
    elif event.source.type == 'user':
        uid = event.source.user_id
        reply = make_reply('user', uid, event.message.text)
    elif event.source.type == 'group':
        gid = event.source.group_id
        reply = make_reply('group', gid, event.message.text)

    if not reply:
        return
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))

def make_reply(type, uid, msg):
    if '小路占卜'.decode('utf-8') in msg:
        global maple_phrase
        # profile = line_bot_api.get_profile(uid)
        random.seed(os.urandom(5))
        ph = random.choice(maple_phrase)
        return '今日運勢：{}'.decode('utf-8').format(ph.decode('utf-8'))
    #if '查'.decode('utf-8') in msg:
    #    profile = line_bot_api.get_profile(uid)
    #    print(profile.__dict__)
    #    return '{} 的顯圖：{}, 狀態：{}'.decode('utf-8').format(profile.display_name, profile.picture_url, profile.status_message)
    elif msg == '可以幫我QQ嗎':
        return '幫QQ喔'
    elif '魔法'.decode('utf-8') in msg:
        return '僕と契約して、魔法少女になってよ！'
    elif 'ㄆㄆ'.decode('utf-8') in msg:
        return 'gmail!'
    elif '請問為什麼'.decode('utf-8') in msg:
        random.seed(os.urandom(5))
        return '因為{}。'.format(random.choice(wtf_reason))
    else:
        return None
