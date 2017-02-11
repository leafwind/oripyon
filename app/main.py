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

hourse_phrase = [
'一馬當先', '千軍萬馬', '天馬行空', '心猿意馬', '犬馬之勞', '汗馬功勞', '老馬識途', '兵荒馬亂', '快馬加鞭', '求馬唐肆', '走馬上任', '走馬平川', '走馬看花', '車水馬龍', '招兵買馬', '金戈鐵馬', '青梅竹馬', '非驢非馬', '指鹿為馬', '害群之馬', '秣馬厲兵', '厲兵秣馬', '馬不停蹄', '馬耳東風', '馬到成功', '馬革裏屍', '馬首是瞻', '馬齒徒長', '單槍匹馬', '蛛絲馬跡', '塞翁失馬', '萬馬奔騰', '駟馬難追', '龍馬精神', '聲色犬馬', '懸崖勒馬', '露出馬腳', '牝牡驪黃'
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
        global hourse_phrase
        # profile = line_bot_api.get_profile(uid)
        random.seed(os.urandom(5))
        ph = random.choice(hourse_phrase)
        return '今日運勢：{}'.decode('utf-8').format(ph.decode('utf-8'))
    #if '查'.decode('utf-8') in msg:
    #    profile = line_bot_api.get_profile(uid)
    #    print(profile.__dict__)
    #    return '{} 的顯圖：{}, 狀態：{}'.decode('utf-8').format(profile.display_name, profile.picture_url, profile.status_message)
    elif 'QQ' in msg:
        return '幫QQ喔'
    elif '魔法'.decode('utf-8') in msg:
        return '僕と契約して、魔法少女になってよ！'
    elif 'ㄆㄆ'.decode('utf-8') in msg:
        return 'gmail!'
    else:
        return None
