import json
import logging
import os
import random

import cachetools.func
import gspread
from linebot.models import FlexSendMessage, BubbleContainer, BoxComponent, \
    ImageComponent, TextComponent, SeparatorComponent

from app.utils.gspread_util import auth_gss_client
from constants import HUGE_GROUP_IDS, TEACHER_HO, PAN_SENTENCES, GSPREAD_KEY_CAT, GOOGLE_AUTH_JSON_PATH, \
    GSPREAD_KEY_SCHUMI, GSPREAD_KEY_SINOALICE

tarot_cards = json.load(open('app/tarot.json', encoding='utf8'))


def touch_schumi():
    random.seed(os.urandom(5))
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    gss_client = auth_gss_client(GOOGLE_AUTH_JSON_PATH, gss_scopes)
    sh = gss_client.open_by_key(GSPREAD_KEY_SCHUMI)
    worksheet = sh.worksheet("摸朽咪")
    list_of_lists = worksheet.get_all_values()
    list_of_lists = list_of_lists[1:]

    population = []
    weights = []
    for w, text in list_of_lists:
        weights.append(float(w))
        population.append(text)
    text = random.choices(population=population, weights=weights, k=1)[0]
    replies = [('text', text)]
    return replies


@cachetools.func.ttl_cache(ttl=86400)
def get_sinoalice_char_list():
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    gss_client = auth_gss_client(GOOGLE_AUTH_JSON_PATH, gss_scopes)
    sh = gss_client.open_by_key(GSPREAD_KEY_SINOALICE)
    worksheet = sh.worksheet("name")
    return worksheet.get_all_values()


@cachetools.func.ttl_cache(ttl=86400)
def get_sinoalice_char_voice_list(name):
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    gss_client = auth_gss_client(GOOGLE_AUTH_JSON_PATH, gss_scopes)
    sh = gss_client.open_by_key(GSPREAD_KEY_SINOALICE)
    try:
        worksheet = sh.worksheet(name)
        char_voice_list = worksheet.get_all_values()
        return char_voice_list
    except gspread.exceptions.WorksheetNotFound:
        return None


def build_sinoalice_char_content(image_url, title):
    container = BubbleContainer(
        direction='ltr',
        hero=ImageComponent(
            url=image_url,
            size='full',
            aspect_ratio='16:19',
            aspect_mode='cover'
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(text=title, weight='bold', size='xl'),
            ],
        ),
    )
    return container


def draw_sinoalice():
    random.seed(os.urandom(5))
    char_list = get_sinoalice_char_list()
    char = random.choice(char_list)
    char_voice_list = get_sinoalice_char_voice_list(char[1])

    image_url = f'https://leafwind.github.io/images/sinoalice/{int(char[0]):0>3d}.png'
    title = f'{char[1]}/{char[2]}'
    container = build_sinoalice_char_content(image_url, title)
    replies = [
        ('flex', FlexSendMessage(alt_text='請到手機確認你的老婆', contents=container))
    ]
    if char_voice_list:
        audio_url = random.choice(char_voice_list)[0]
        replies.append(
            ('audio', f'{audio_url}')
        )
    return replies


def find_schumi():
    random.seed(os.urandom(5))
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    gss_client = auth_gss_client(GOOGLE_AUTH_JSON_PATH, gss_scopes)
    sh = gss_client.open_by_key(GSPREAD_KEY_SCHUMI)
    worksheet = sh.worksheet("找朽咪")
    list_of_lists = worksheet.get_all_values()
    list_of_lists = list_of_lists[1:]

    population = []
    weights = []
    for w, text in list_of_lists:
        weights.append(float(w))
        population.append(text)
    text = random.choices(population=population, weights=weights, k=1)[0]
    replies = [('text', text)]
    return replies


def draw_cat():
    random.seed(os.urandom(5))
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    gss_client = auth_gss_client(GOOGLE_AUTH_JSON_PATH, gss_scopes)
    sh = gss_client.open_by_key(GSPREAD_KEY_CAT)
    worksheet = sh.get_worksheet(0)
    list_of_lists = worksheet.get_all_values()
    list_of_lists = list_of_lists[1:]
    row = random.choice(list_of_lists)
    if row[1]:
        replies = [('image', row[0]), ('text', row[1])]
    else:
        replies = [('image', row[0])]
    return replies


def draw_card(msg_info):
    random.seed(os.urandom(5))
    msg = random.choice(TEACHER_HO)
    return msg.format(name=msg_info.user_name)


def pan_pan():
    random.seed(os.urandom(5))
    msg = random.choice(PAN_SENTENCES)
    return msg


def tarot(msg_info):
    random.seed(os.urandom(5))
    card = random.choice(tarot_cards)
    logging.info('%s: %s', card['nameCN'], card['url'])
    replies = []
    if msg_info.source_id not in HUGE_GROUP_IDS:
        # skip card picture for large groups
        replies.append(('image', card['url']))
    replies.append(('text', f'{card["nameCN"]}: {card["conclusion"]}'))
    return replies


def coc_7e_basic(msg):
    random.seed(os.urandom(5))
    d100 = random.randint(1, 100)  # 1 <= N <= 100
    condition = int(msg.split('<=')[1])
    result = f'克蘇魯的呼喚七版：(1D100<={condition}) 初始結果 → {d100}\n'

    final_dice = d100
    if '(' in msg:
        extra = int(msg.split(')')[0].split('(')[1])
        if -2 <= extra <= 2 and extra != 0:
            tens_digit = d100 // 10
            abs_extra = abs(extra)
            extra_dices = [random.randint(1, 10) for _ in range(abs_extra)]
            if extra < 0:
                extra_dice_desc = '懲罰骰取高'
                tens_digit = max(tens_digit, max(extra_dices))
            else:
                extra_dice_desc = '獎勵骰取低'
                tens_digit = min(tens_digit, min(extra_dices))
            final_dice = tens_digit * 10 + d100 % 10
            result += f'→ 十位數加骰為{"、".join([str(d*10) for d in extra_dices])}，{extra_dice_desc} → 最終值({str(final_dice)})'

    if final_dice == 1:
        final_stat = ' → ＼大★成★功／'
    elif final_dice == 100:
        final_stat = ' → 大失敗，すばらしく運がないな、君は。'
    elif final_dice <= condition // 5:
        final_stat = ' → 極限成功'
    elif final_dice <= condition // 2:
        final_stat = ' → 困難成功'
    elif final_dice <= condition:
        final_stat = ' → 一般成功'
    elif final_dice > condition:
        final_stat = ' → 失敗'
    else:
        raise ValueError(f'invalid final_dice range: {final_dice}')
    result += final_stat
    return result


def nca():
    random.seed(os.urandom(5))
    d10 = random.randint(1, 10)  # 1 <= N <= 10
    desc_str_map = {
        1: '大失敗\n命中包含自己的友方，由被攻擊方選擇被命中的部位。',
        2: '失敗\n未命中',
        3: '失敗\n未命中',
        4: '失敗\n未命中',
        5: '失敗\n未命中',
        6: '成功\n由被攻擊方選擇被命中的部位。',
        7: '成功\n命中腳部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
        8: '成功\n命中胴部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
        9: '成功\n命中腕部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
        10: '成功\n命中頭部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
    }
    return f'死靈年代記之永遠的後日談：[{d10}]  → {desc_str_map[d10]}'


def choice(matched_msg):
    random.seed(os.urandom(5))
    options_str = matched_msg.split('[')[1][:-1]
    options = options_str.split(',')
    result = f'自訂選項：[{",".join(options)}] → {random.choice(options)}'
    return result


def fortune():
    random.seed(os.urandom(5))
    dice = random.randint(1, 1000)  # 1 <= N <= 1000
    ans = [
        '／(˃ᆺ˂)＼大吉だよ！\nやったね⭐︎',
        '／(^ x ^=)＼大吉……騙你的，差一點呢！\n只是吉而已呦',
        '／(^ x ^)＼吉。🎉\n很棒呢！',
        '／(･ × ･)＼中吉。\n朽咪覺得還不錯吧。(ゝ∀･)',
        '／(･ × ･)＼小吉。\n就是小吉，平淡過日子，願世界和平。☮',
        '／(･ × ･)＼半吉。\n㊗️朽咪祝福你！',
        '／(･ × ･)＼末吉。\n嗯～勉勉強強吧！',
        '／(･ × ･)＼末小吉。\n至少不壞呢！',
        '／(=´x`=)＼凶。\n往好處想，至少還有很多更糟的！',
        '／(=´x`=)＼小凶。\n運氣不是很好呢，怎麼辦？',
        '／(=´x`=)＼半凶。\n有點糟糕～',
        '／(=´x`=)＼末凶。\n運氣真差阿...幫QQ',
        '／人◕ ‿‿ ◕人＼ 大凶⁉️僕と契約して、魔法少女になってよ！'
    ]
    if dice <= 20:
        return ans[0]
    elif dice <= 100:
        return ans[1]
    elif dice <= 200:
        return ans[2]
    elif dice <= 300:
        return ans[3]
    elif dice <= 400:
        return ans[4]
    elif dice <= 500:
        return ans[5]
    elif dice <= 600:
        return ans[6]
    elif dice <= 700:
        return ans[7]
    elif dice <= 800:
        return ans[8]
    elif dice <= 850:
        return ans[9]
    elif dice <= 900:
        return ans[10]
    elif dice <= 950:
        return ans[11]
    elif dice <= 1000:
        return ans[12]
    else:
        raise ValueError
