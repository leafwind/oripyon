from app.common_reply import get_reply_from_mapping_function
from app.rabbit import my_rabbit, adopt_rabbit
from message_generator import flex_message_generator

from linebot.models import (
    FlexSendMessage, CarouselContainer
)


def build_top_menu_function_card_message_tool(_msg_info, _robot_settings):
    title = '工具'
    text_content = [
        [
            ('水庫', '水庫'),
        ],
        [
            ('匯率', '匯率'),
        ]
    ]
    bubble1 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content,
                                                                          bubble_size='micro')
    title = '氣象圖'
    text_content = [
        [
            ('天氣', '天氣'),
        ],
        [
            ('即時雨量', '即時雨量'),
        ],
        [
            ('雷達', '雷達'),
        ],
        [
            ('空品', '空品'),
        ]
    ]
    bubble2 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content,
                                                                          bubble_size='micro')
    carousel_container = CarouselContainer([bubble1, bubble2])
    return [('flex', FlexSendMessage(alt_text='工具類別指令範例', contents=carousel_container))]


def build_top_menu_function_card_message_dice(_msg_info, _robot_settings):
    title = '運勢？'
    text_content = [
        [
            ('運勢', '運勢 考試'),
            ('塔羅', '塔羅 上班'),
        ],
    ]
    bubble1 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content,
                                                                          bubble_size='nano')
    title = '占卜？'
    text_content = [
        [
            ('為什麼', '請問為什麼會下雨'),
            ('何老師', '何老師抽卡'),
        ],
    ]
    bubble2 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content,
                                                                          bubble_size='nano')
    title = '骰子？'
    text_content = [
        [('choice', 'choice[排骨飯,豬腳飯,焢肉飯]')],
        [('NCA', 'NCA 攻擊小明')],
        [('cc<x', 'cc<=50')],
    ]
    bubble3 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content,
                                                                          bubble_size='nano')
    carousel_container = CarouselContainer([bubble1, bubble2, bubble3])
    return [('flex', FlexSendMessage(alt_text='運勢類別指令範例', contents=carousel_container))]


def build_top_menu_function_card_message_others(_msg_info, _robot_settings):
    title = '莫名？'
    text_content = [
        [
            ('幫QQ', '幫QQ'),
        ],
        [
            ('爛中文', '爛中文'),
        ]
    ]
    bubble1 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content,
                                                                          bubble_size='nano')

    title = '魔法？'
    text_content = [
        [
            ('咕嚕靈波', '咕嚕靈波'),
        ],
        [
            ('魔法少女', '魔法少女'),
        ],
    ]
    bubble2 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content,
                                                                          bubble_size='nano')
    title = '還願？'
    text_content = [
        [
            ('慈孤觀音', '慈孤觀音'),
        ],
        [
            ('女兒紅', '女兒紅'),
        ]
    ]
    bubble3 = flex_message_generator.build_top_menu_function_card_content(title=title, text_contents=text_content,
                                                                          bubble_size='nano')

    carousel_container = CarouselContainer([bubble1, bubble2, bubble3])

    return [('flex', FlexSendMessage(alt_text='彩蛋類別指令範例', contents=carousel_container))]


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
