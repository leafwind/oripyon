import re
import os
import random
import json
import logging

from linebot.models import (
    TextSendMessage, ImageSendMessage, TemplateSendMessage
)

from linebot.exceptions import (
    LineBotApiError
)

from app.line_templates import make_template_action, make_carousel_column
from app.line_templates import make_carousel_template, make_confirm_template, make_buttons_template
from app.phrase import horse_phrase, lion_phrase, dunkey_phrase
from app.emoji_list import cry_emoji_list

maple_phrase = horse_phrase + lion_phrase + dunkey_phrase
help_find_pattern = re.compile('協尋')


RANDOM_GF = {}
random_gf_file = os.path.join('line-user-info', 'random_gf.json')
if os.path.exists(random_gf_file):
    with open(random_gf_file, 'r') as f:
        RANDOM_GF = json.load(f)


def group_reply_test(_line_bot_api, _source_id, _uid, msg):
    if msg == '!hinet':
        image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/BFTQEnG.png',
            preview_image_url='https://i.imgur.com/BFTQEnG.png',
        )
        return [image_message]

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


def group_reply_lineage_m(_line_bot_api, _source_id, _uid, _msg):
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


def group_reply_mao_sino_alice(_line_bot_api, _source_id, _uid, msg):
    replies = None
    if '小米米' in msg:
        replies = ['綁起來電擊烤焦爆香切段上菜（¯﹃¯）']
    elif '2050' in msg:
        replies = [
            '兩洞伍洞，部隊起床｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡',
            '睡你麻痺起來嗨ヽ(`Д´)ノ',
        ]
    elif '夢魘順序' in msg:
        replies = ['sky降攻 -> 普爾加防 -> 米米(工讀生)黑腕 -> 芙溫妖精王 -> 邱御豪降防']
    elif '死愛資料庫' in msg:
        replies = ['https://sinoalice.game-db.tw/']
    elif '狗糧' == msg:
        replies = ['07:30, 12:00, 19:30, 22:30, 01:00 持續半小時 ／人◕ ‿‿ ◕人＼']
    elif '素材' == msg:
        replies = ['武器(風)：一、三、六\n武器(火)：二、四、日\n武器(水)：三、五、日\n防具：二、四、六\n金幣：一、五、六 ／人◕ ‿‿ ◕人＼']
    else:
        pass

    if replies:
        return [TextSendMessage(text=r) for r in replies]
    else:
        return []


def group_reply_taiwan_sino_alice(_line_bot_api, _source_id, _uid, msg):
    replies = None
    if '死愛資料庫' in msg:
        replies = ['https://sinoalice.game-db.tw/']
    elif '狗糧' == msg:
        replies = ['07:30, 12:00, 19:30, 22:30, 01:00 持續半小時 ／人◕ ‿‿ ◕人＼']
    elif '素材' == msg:
        replies = ['武器(風)：一、三、六\n武器(火)：二、四、日\n武器(水)：三、五、日\n防具：二、四、六\n金幣：一、五、六 ／人◕ ‿‿ ◕人＼']
    else:
        pass

    if replies:
        return [TextSendMessage(text=r) for r in replies]
    else:
        return []


def group_reply_nier_sino_alice(line_bot_api, source_id, uid, msg):
    msg = msg.lower()
    random.seed(os.urandom(5))
    wanted_list = ['頓頓', '名字', '雞排', '來來', '盼盼', '四姐', '四姊', 'EBB', '鈴']
    male_list = ['芙芙', '性迪', '阿星', '肉肉', '肉凱', '糕連']
    female_list = ['名字', '盼盼', '四姐', 'EBB', '鈴♡', '凝凝', '楓楓', '丸丸']
    asexual_list = ['丶丶', '丿丿', '樹樹', '兔比', '小葵', '雞排', 'Momo']
    all_list = male_list + female_list + asexual_list
    id_list = [
        '四姊 963028424',
        '頓頓 208404895',
        'stCarP 329543491',
        '夜貓先生 832644419',
        '撇撇 121381885',
        '楓楓 694730233',
        '西門(愛睏狼) 403332013',
        '10(Lan Shawn) 372629712',
        '火腿通粉(肉凱) 589363711',
        '肉肉 220242535',
        'redyee 866447142',
        'ひまわり(小葵) 906443893',
        '群草(Bosco) 820394786',
        '微風輕語(微笑) 519184032',
        '我才不告訴你累(陳俊傑) 494857518',
        '群青(盼盼) 243719941',
        '獄剎(呂立升) 284290895',
        '\名字/ 807235479',
        '冬瓜拿鐵 469089830',
        'ハツキ 844936402',
        '多多綠少了多多(米卡狗) 376103475',
        '丸子u(采薇丸) 295185564',
        '莉芙溫 467287876'
    ]
    replies = None
    if '我的' in msg or '誰的' in msg:
        for name in wanted_list:
            if name in msg:
                if name == '盼盼':
                    if random.random() >= 0.2:
                        replies = [f'已經是她們會長的形狀了 {random.choice(cry_emoji_list)}']
                    else:
                        replies = ['拿杖敲爆你的腦殼 O-(///￣皿￣)⊃━☆ﾟ.*･｡']
                elif name in ['四姐', '四姊']:
                    replies = ['永遠單身的小秘書 (●´ω｀●)ゞ']
                elif name == 'EBB':
                    replies = ['不要潛水出來嗨 ヽ(∀ﾟ )人(ﾟ∀ﾟ)人( ﾟ∀)人(∀ﾟ )人(ﾟ∀ﾟ)人( ﾟ∀)ﾉ']
                else:
                    replies = ['是我的！！']
    elif '雞排' in msg and '吃' in msg:
        replies = ['我也要吃 (๑´ڡ`๑)']
    elif msg.startswith('抽男'):
        replies = [f'(੭•̀ω•́)੭ 恭喜你，是{random.choice(male_list)}呢！']
    elif msg.startswith('抽女'):
        replies = [f'(੭•̀ω•́)੭ 恭喜你，是{random.choice(female_list)}呢！']
    elif msg.startswith('抽不明'):
        replies = [f'(੭•̀ω•́)੭ 恭喜你，是{random.choice(asexual_list)}呢！']
    elif msg.startswith('抽全部'):
        replies = [f'(੭•̀ω•́)੭ 恭喜你，是{random.choice(all_list)}呢！']
    elif '死愛資料庫' in msg:
        replies = ['https://sinoalice.game-db.tw/']
    elif '狗糧' == msg:
        replies = ['07:30, 12:00, 19:30, 22:30, 01:00 持續半小時 ／人◕ ‿‿ ◕人＼']
    elif '素材' == msg:
        replies = ['武器(風)：一、三、六\n武器(火)：二、四、日\n武器(水)：三、五、日\n防具：二、四、六\n金幣：一、五、六 ／人◕ ‿‿ ◕人＼']
    elif msg.startswith('id對照表'):
        replies = ['\n'.join(id_list)]
    else:
        pass
    if msg.startswith('抽女友'):
        try:
            user_name = line_bot_api.get_group_member_profile(source_id, uid).display_name
        except LineBotApiError as e:
            logging.error('LineBotApiError: %s', e)
            user_name = ''
        # drop the user itself
        candidates = RANDOM_GF  # copy a new obj
        for i, c in enumerate(candidates):
            if c['uid'] == uid:
                logging.info(f'{user_name} 丟掉自己 {c["name"]}')
                candidates.pop(i)
                break
        target = random.choice(list(candidates))
        target_name = target['name']
        url = target['url']
        msg = f'{user_name}真可憐呢沒有女友，不哭不哭(´;ω;`)ヾ(･∀･`)\n給你一個{target_name}的左手聞香'
        if 'custom_msg' in target:
            msg += f'\n{target["custom_msg"]}'
        return [
            ImageSendMessage(original_content_url=url, preview_image_url=url),
            TextSendMessage(text=msg)
        ]
    if replies:
        return [TextSendMessage(text=r) for r in replies]
    else:
        return []

def group_reply_luna(_line_bot_api, _source_id, _uid, msg):
    if '涼哥' in msg:
        return [TextSendMessage(text='正直善良又誠懇、不會說話卻實在')]
    return


def group_reply_mao(_line_bot_api, _source_id, _uid, _msg):
    return


def group_reply_working(_line_bot_api, _source_id, _uid, _msg):
    return

    
def group_reply_mao_test(_line_bot_api, _source_id, _uid, _msg):
    return 

