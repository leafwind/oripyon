import json
import logging
import os
import random
import re

from linebot.models import (
    TextSendMessage, ImageSendMessage, TemplateSendMessage
)

from app.line_templates import make_carousel_template, make_confirm_template, make_buttons_template
from app.line_templates import make_template_action, make_carousel_column
from app.phrase import horse_phrase, lion_phrase, dunkey_phrase

maple_phrase = horse_phrase + lion_phrase + dunkey_phrase
help_find_pattern = re.compile('協尋')
from constants import SINOALICE_NIER_ID_LIST

RANDOM_GF = {}
random_gf_file = os.path.join('line-user-info', 'random_gf.json')
if os.path.exists(random_gf_file):
    with open(random_gf_file, 'r') as f:
        RANDOM_GF = json.load(f)

RANDOM_LEG = {}
random_leg_file = os.path.join('line-user-info', 'random_leg.json')
if os.path.exists(random_leg_file):
    with open(random_leg_file, 'r') as f:
        RANDOM_LEG = json.load(f)

RANDOM_COLLARBONE = {}
random_collarbone_file = os.path.join('line-user-info', 'random_collarbone.json')
if os.path.exists(random_collarbone_file):
    with open(random_collarbone_file, 'r') as f:
        RANDOM_COLLARBONE = json.load(f)


def group_reply_test(_line_bot_api, _source_id, _uid, msg):
    leafwind_photo_url = \
        'https://static-cdn.jtvnw.net/jtv_user_pictures/panel-145336656-image-e9329cd5f8f44a76-320-320.png'
    kaori_photo_url = \
        'https://static-cdn.jtvnw.net/jtv_user_pictures/panel-145336656-image-4808e3743f50232e-320-320.jpeg'
    uri_action = make_template_action('uri', '前往卡歐的首頁', uri='http://yfting.com')
    uri_action2 = make_template_action('uri', '前往玉米的首頁', uri='https://data.leafwind.tw')
    postback_action = make_template_action('postback', 'ping', data='ping')
    postback_action_with_text = make_template_action('postback', 'ping with text', data='ping', text='ping')
    message_action = make_template_action('message', 'Translate Rice', text='米')
    if msg == 'carousel':
        col1 = make_carousel_column('這是卡歐', 'Hi~', [uri_action, postback_action], kaori_photo_url)
        col2 = make_carousel_column('這是玉米', 'ㄏㄏ', [uri_action2, message_action], leafwind_photo_url)

        carousel_template = make_carousel_template([col1, col2])

        template_message = TemplateSendMessage(
            alt_text='carousel alt text', template=carousel_template)
        return [template_message]

    elif msg == 'confirm':  # left / right buttons
        message_action = make_template_action('message', '是', text='帥！')
        message_action2 = make_template_action('message', '否', text='帥！')
        confirm_template = make_confirm_template('玉米帥嗎？', [message_action, message_action2])
        template_message = TemplateSendMessage(
            alt_text='confirm alt text', template=confirm_template)
        return [template_message]

    elif msg == 'buttons':  # top-down buttons
        buttons_template = make_buttons_template(
            'My buttons sample',
            'Hello, my buttons',
            [uri_action, postback_action, postback_action_with_text, message_action],
            leafwind_photo_url
        )
        template_message = TemplateSendMessage(
            alt_text='buttons alt text', template=buttons_template)
        return [template_message]

    return []


def group_reply_maplestory(_line_bot_api, _source_id, _uid, msg):
    if '小路占卜' in msg:
        global maple_phrase
        random.seed(os.urandom(5))
        ph = random.choice(maple_phrase)
        msg = f'今日運勢：{ph}'
        return [TextSendMessage(text=msg)]
    else:
        return []


def group_reply_yebai(_line_bot_api, _source_id, _uid, msg):
    if help_find_pattern.search(msg):
        image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/ksIHMn6.jpg',
            preview_image_url='https://i.imgur.com/ksIHMn6.jpg',
        )
        return [
            image_message,
            TextSendMessage(text='請幫幫忙找找他...等等他是誰？(((ﾟДﾟ;)))')
        ]


def _group_reply_sino_alice_base(msg):
    replies = []
    if '死愛資料庫' == msg:
        replies = [TextSendMessage(text='https://sinoalice.game-db.tw/')]
    elif '狗糧' == msg:
        replies = [TextSendMessage(text='07:30, 12:00, 19:30, 22:30, 01:00 持續半小時 ／人◕ ‿‿ ◕人＼')]
    elif '素材' == msg:
        replies = [TextSendMessage(text='武器(風)：一、三、六\n武器(火)：二、四、日\n武器(水)：三、五、日\n防具：二、四、六\n金幣：一、五、六 ／人◕ ‿‿ ◕人＼')]
    else:
        pass
    return replies


def group_reply_mao_sino_alice(_line_bot_api, _source_id, _uid, msg):
    if '小米米' in msg:
        replies = [TextSendMessage(text='綁起來電擊烤焦爆香切段上菜（¯﹃¯）')]
    elif '2050' in msg:
        replies = [
            TextSendMessage(text='兩洞伍洞，部隊起床｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡'),
            TextSendMessage(text='睡你麻痺起來嗨ヽ(`Д´)ノ'),
        ]
    elif '2150' in msg:
        replies = [
            TextSendMessage(text='兩么伍洞，部隊起床｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡'),
            TextSendMessage(text='普爾喵子睡你麻痺起來嗨ヽ(`Д´)ノ'),
        ]
    elif '2250' in msg:
        replies = [
            TextSendMessage(text='二二伍洞，部隊起床｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡'),
            TextSendMessage(text='芙溫睡你麻痺起來嗨ヽ(`Д´)ノ'),
        ]
    elif '夢魘順序' in msg:
        replies = [TextSendMessage(text='sky降攻 -> 普爾加防 -> 芙溫妖精王-> 米米(工讀生)黑腕  -> 邱御豪降防')]
    else:
        replies = _group_reply_sino_alice_base(msg)
    return replies


def group_reply_nier_sino_alice(_line_bot_api, _source_id, _uid, msg):
    if msg.lower().startswith('id對照表'):
        replies = [TextSendMessage(text='\n'.join(SINOALICE_NIER_ID_LIST))]
    else:
        replies = _group_reply_sino_alice_base(msg)
    return replies


def group_reply_mao(_line_bot_api, _source_id, _uid, _msg):
    return


def group_reply_default(_line_bot_api, _source_id, _uid, _msg):
    return


def random_choice_except_key(from_dict, except_key):
    # drop the user itself
    random.seed(os.urandom(5))
    candidates = from_dict  # copy a new obj
    for i, c in enumerate(candidates):
        if c['uid'] == except_key:
            logging.info(f'丟掉自己 {c["name"]}')
            candidates.pop(i)
    target = random.choice(list(candidates))
    return target


GROUP_MAPPING = {
    'C1bebaeaf89242089f0d755d492df6cb6': {
        'name': '測試群組',
        'function': group_reply_test,
        'log_filename': 'powpow_test',
    },
    'C25add4301bc790a641e07b02b868a9b7': {
        'name': '葉白',
        'function': group_reply_yebai,
        'log_filename': 'yebai',
    },
    'C0cd56d37156c5ad3fe04b702624d50dd': {
        'name': '小路北七群',
        'function': group_reply_maplestory,
        'log_filename': 'maplestory',
    },
    'Cfb6a76351d112834244144a1cd4f0f57': {
        'name': '死愛魔王城',
        'function': group_reply_mao_sino_alice,
        'log_filename': 'mao_sino_alice',
    },
    'C1e38a92f8c7b4ad377df882b9f3bf336': {
        'name': '尼爾主題餐廳',
        'function': group_reply_nier_sino_alice,
        'log_filename': 'nier_sino_alice',
    },
    'Cbc420349e56f3bae5d5f46fafb0ac5cb': {
        'name': '社畜人生的煩惱',
        'function': group_reply_default,
        'log_filename': 'worker_life',
    },
    'Cfbbdac072c508472fd3acc9ac8fa7adc': {
        'name': '二代魔王城',
        'function': group_reply_mao,
        'log_filename': 'mao',
    },
    'Cf794cf7dc1970c3fba9122673cf3dcde': {
        'name': '魔王城測試',
        'function': group_reply_default,
        'log_filename': 'mao_test',
    },
    'C01f5f627f97916d0a6b2f40228656bc0': {
        'name': '死愛甜甜圈',
        'function': group_reply_default,
        'log_filename': 'schumi_user',
    }
}