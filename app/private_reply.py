from app.common_reply import get_reply_from_mapping_function
from app.rabbit import my_rabbit, adopt_rabbit
from message_generator import flex_message_generator

from linebot.models import (
    FlexSendMessage, CarouselContainer
)


def build_top_menu_function_card_message_tool(_msg_info, _robot_settings):
    title = '工具類別指令範例'
    text_content = [
        [
            ('水庫(beta)', '水庫'),
            ('匯率(beta)', '匯率'),
        ],
    ]
    bubble1 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content)
    title = '氣象指令(中央氣象局圖檔)'
    text_content = [
        [
            ('天氣', '天氣'),
            ('即時雨量', '即時雨量'),
        ],
        [
            ('雷達', '雷達'),
            ('空品', '空品'),
        ],
    ]
    bubble2 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content)
    carousel_container = CarouselContainer([bubble1, bubble2])
    return [('flex', FlexSendMessage(alt_text='工具類別指令範例', contents=carousel_container))]


def build_top_menu_function_card_message_dice(_msg_info, _robot_settings):
    title = '運勢類別指令範例'
    text_content = [
        [
            ('運勢', '運勢 考試'),
            ('塔羅', '塔羅 上班'),
        ],
        [
            ('請問為什麼', '請問為什麼會下雨'),
            ('何老師抽卡', '何老師抽卡'),
        ],
        [
            ('摸朽咪', '摸朽咪'),
            ('找朽咪', '找朽咪'),
        ],
    ]
    bubble1 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content)

    title = '骰子類別指令範例'
    text_content = [
        [('choice[x,y,z]', 'choice[排骨飯,豬腳飯,焢肉飯]')],
        [('NCA [隨意] (攻擊檢定)', 'NCA 攻擊小明')],
        [('cc(z)<=x (COC 7e)', 'cc<=50')],
    ]
    bubble2 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content)
    carousel_container = CarouselContainer([bubble1, bubble2])
    return [('flex', FlexSendMessage(alt_text='運勢類別指令範例', contents=carousel_container))]


def build_top_menu_function_card_message_others(_msg_info, _robot_settings):
    title = '彩蛋類別指令範例'
    text_content = [
        [
            ('幫QQ', '幫QQ'),
            ('爛中文', '爛中文'),
        ],
        [
            ('咕嚕靈波', '咕嚕靈波'),
            ('魔法少女', '魔法少女'),
        ],
        [
            ('慈孤觀音', '慈孤觀音'),
            ('女兒紅', '女兒紅'),
        ],
    ]
    container = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content)
    return [('flex', FlexSendMessage(alt_text='彩蛋類別指令範例', contents=container))]


pattern_mapping_private = [
    {
        'cmd': '我的兔子',
        'type': 'equal',
        'function': my_rabbit,
        'multi_type_output': True
    },
    {
        'cmd': '領養兔子',
        'type': 'equal',
        'function': adopt_rabbit,
        'multi_type_output': True
    },
    {
        'cmd': '運勢類別指令',
        'type': 'equal',
        'function': build_top_menu_function_card_message_dice,
        'multi_type_output': True
    },
    {
        'cmd': '工具類別指令',
        'type': 'equal',
        'function': build_top_menu_function_card_message_tool,
        'multi_type_output': True
    },
    {
        'cmd': '彩蛋類別指令',
        'type': 'equal',
        'function': build_top_menu_function_card_message_others,
        'multi_type_output': True
    }
]


def private_reply(msg_info, robot_settings):
    reply = get_reply_from_mapping_function(msg_info, robot_settings, pattern_mapping_private)
    if reply:
        return reply
