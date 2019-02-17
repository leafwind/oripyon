import re
import time
import logging

from linebot.models import (
    TextSendMessage, ImageSendMessage
)

from app.dice import fortune, tarot, nca, choice
from app.finance import exchange_rate
from app.direct_reply import gurulingpo, poor_chinese, qq, mahoshoujo, why, bot_help
from app.weather_status import weather_now, rainfall_now, radar_now, aqi_now, aqi_predict, aqi_status


# equivalent to:
# fortune_pattern = re.compile(ur'\u904b\u52e2', re.UNICODE)
fortune_pattern = re.compile(r'運勢')
tarot_pattern = re.compile(r'塔羅')
gurulingpo_pattern = re.compile(r'咕嚕靈波')
mahoshoujo_pattern = re.compile(r'魔法少女')
why_pattern = re.compile(r'請問為什麼')
help_pattern = re.compile(r'/help')
poor_chinese_pattern = re.compile(r'爛中文')
qq_pattern = re.compile(r'幫qq', re.IGNORECASE)
nca_pattern = re.compile(r'nca')
aqi_predict_pattern = re.compile(r'^空品預測\s+.+')
aqi_status_pattern = re.compile(r'^空品現況\s+.+')
choice_pattern = re.compile(r"""choice\s?  # choice + 0~1 space
                            \[             # [
                            [^,\[\]]+      # not start with , [, ] (at least once)
                            (,[^,\[\]]+)+  # plus dot (at least once)
                            ]              # ]
                            """, re.VERBOSE | re.IGNORECASE)
pattern_mapping = [
    {
        'cmd': fortune_pattern,
        'type': 'search',
        'function': fortune,
    },
    {
        'cmd': nca_pattern,
        'type': 'search',
        'function': nca,
    },
    {
        'cmd': gurulingpo_pattern,
        'type': 'search',
        'function': gurulingpo
    },
    {
        'cmd': choice_pattern,
        'type': 'search',
        'function': choice,
        'matched_as_arg': True
    },
    {
        'cmd': '天氣',
        'type': 'equal',
        'function': weather_now
    },
    {
        'cmd': '即時雨量',
        'type': 'equal',
        'function': rainfall_now
    },
    {
        'cmd': '雷達',
        'type': 'equal',
        'function': radar_now
    },
    {
        'cmd': '空品',
        'type': 'equal',
        'function': aqi_now
    },
    {
        'cmd': aqi_predict_pattern,
        'type': 'search',
        'function': aqi_predict,
        'matched_as_arg': True
    },
    {
        'cmd': aqi_status_pattern,
        'type': 'search',
        'function': aqi_status,
        'matched_as_arg': True,
        'multi_type_output': True
    },
    {
        'cmd': '匯率',
        'type': 'equal',
        'function': exchange_rate
    },
    {
        'cmd': poor_chinese_pattern,
        'type': 'search',
        'function': poor_chinese
    },
    {
        'cmd': qq_pattern,
        'type': 'search',
        'function': qq
    },
    {
        'cmd': mahoshoujo_pattern,
        'type': 'search',
        'function': mahoshoujo
    },
    {
        'cmd': why_pattern,
        'type': 'search',
        'function': why
    },
    {
        'cmd': help_pattern,
        'type': 'search',
        'function': bot_help
    },
]

last_msg = {}
replied_time = {}


def build_complex_msg(result):
    complex_msg = []
    for msg_type, msg in result:
        if msg_type == 'text':
            complex_msg.append(TextSendMessage(text=msg))
        elif msg_type == 'image':
            complex_msg.append(ImageSendMessage(
                original_content_url=msg,
                preview_image_url=msg,
            ))
        else:
            raise ValueError(f" unknown msg_type: {msg_type}")
    return complex_msg


def common_reply(source_id, msg):
    now = int(time.time())
    msg = msg.lower()
    if tarot_pattern.search(msg):
        card = tarot()
        image_message = ImageSendMessage(
            original_content_url=card['url'],
            preview_image_url=card['url']
        )
        return [
            image_message,
            TextSendMessage(text=f'{card["nameCN"]}: {card["conclusion"]}')
        ]
    for p in pattern_mapping:
        if p['type'] == 'equal':
            if msg == p['cmd']:
                result = p['function']()
                if p.get('multi_type_output', False):
                    return build_complex_msg(result)
                else:
                    return [TextSendMessage(text=result)]

        elif p['type'] == 'search':
            match = p['cmd'].search(msg)
            if match:
                if p.get('matched_as_arg', False):
                    result = p['function'](match.group(0))
                else:
                    result = p['function']()
                if p.get('multi_type_output', False):
                    return build_complex_msg(result)
                else:
                    return [TextSendMessage(text=result)]
        else:
            raise ValueError(f" unknown pattern type: {p['type']}")

    if msg == last_msg.get(source_id, None):
        logging.info('偵測到重複，準備推齊')
        repeated_diff_ts = now - replied_time.get((source_id, msg), 0)
        if repeated_diff_ts > 600:
            logging.info(f'{msg} 上次重複已經超過 {repeated_diff_ts} 秒，執行推齊！')
            replied_time[(source_id, msg)] = now
            return [TextSendMessage(text=msg)]
        else:
            logging.info(f'{msg} 上次重複在 {repeated_diff_ts} 秒內，不推齊')
    last_msg[source_id] = msg
    return []
