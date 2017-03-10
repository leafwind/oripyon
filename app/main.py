# -*- coding: utf-8 -*-
import os
import random

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, CarouselTemplate, CarouselColumn, URITemplateAction, PostbackTemplateAction, MessageTemplateAction, TemplateSendMessage, ConfirmTemplate, ButtonsTemplate
)

from line_auth_key import CHANNEL_SECRET, CHANNEL_ACCESS_TOKEN
from app.phrase import horse_phrase, lion_phrase, dunkey_phrase
from app import cwb_weather_predictor

maple_phrase = horse_phrase + lion_phrase + dunkey_phrase

wtf_reason = [
    '一例一休',
    '陸客不來了',
    '一個阿嬤嘎挖共，不出來選，天公伯不會原諒我',
    '只要是男人就會喜歡邱主任',
    '車子她開的～我上了她的車～就～咻的滑進摩鐵了',
    '手沒放在鍵盤上不能算工時',
    '然後他就死掉了',
    '我犯了全天下男人都會犯的錯',
    '白海豚會轉彎',
    '我沒講過白海豚會轉彎',
    '一個便當吃不夠，你有沒有吃兩個？',
    '垃圾不分藍綠',
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
    if event.message.text == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        return
    elif event.message.text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageTemplateAction(label='Yes', text='Yes!'),
            MessageTemplateAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        return
    elif event.message.text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        return
    elif event.source.type == 'room':
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
    msg_list = msg.split(' ')
    len_msg = len(msg_list)
    if msg_list[0] == '天氣'.decode('utf-8'):
        return cwb_weather_predictor.predict(msg_list[1].encode('utf-8').replace('台', '臺').decode('utf-8'))
    elif '小路占卜'.decode('utf-8') in msg:
        global maple_phrase
        # profile = line_bot_api.get_profile(uid)
        random.seed(os.urandom(5))
        ph = random.choice(maple_phrase)
        return '今日運勢：{}'.decode('utf-8').format(ph.decode('utf-8'))
    #if '查'.decode('utf-8') in msg:
    #    profile = line_bot_api.get_profile(uid)
    #    print(profile.__dict__)
    #    return '{} 的顯圖：{}, 狀態：{}'.decode('utf-8').format(profile.display_name, profile.picture_url, profile.status_message)
    elif '幫QQ'.decode('utf-8') in msg:
        return '幫QQ喔'
    elif '魔法'.decode('utf-8') in msg:
        return '僕と契約して、魔法少女になってよ！'
    elif 'ㄆㄆ'.decode('utf-8') in msg:
        return 'gmail!'
    elif '請問為什麼'.decode('utf-8') in msg:
        random.seed(os.urandom(5))
        return '因為{}。'.format(random.choice(wtf_reason))
    elif '作運動'.decode('utf-8') in msg or '做運動'.decode('utf-8') in msg:
        return 'https://www.facebook.com/dailyheyhey/videos/1721131438179051'
    elif '中文'.decode('utf-8') in msg:
        return '我覺的台灣人的中文水準以經爛ㄉ很嚴重 大家重來都不重視 因該要在加強 才能越來越利害'
    else:
        return None
