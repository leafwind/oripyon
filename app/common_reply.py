import re
import time
import logging
from datetime import datetime

from linebot.models import (
    TextSendMessage, ImageSendMessage
)

from app.dice import fortune, tarot, nca, choice
from app.finance import exchange_rate
from app.direct_reply import gurulingpo, poor_chinese, qq, mahoshoujo, why, bot_help
from app.weather_status import weather_now, rainfall_now, radar_now, aqi_now
from app import predict_AQI

from taiwan_area_map.query_area import query_area

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


def common_reply(source_id, msg):
    now = int(time.time())
    msg = msg.lower()
    msg_list = msg.split(' ')
    if '空品預測 ' in msg:
        location = msg_list[1].replace('台', '臺')
        aqi_info = predict_AQI.predict_aqi(location)
        if not aqi_info:
            return [TextSendMessage(text='查無資料')]

        predict_time = datetime.fromtimestamp(aqi_info['publish_ts'] + 8 * 3600).strftime('%m/%d %H 時')
        target_time = datetime.fromtimestamp(aqi_info['forecast_ts'] + 8 * 3600).strftime('%m/%d')
        aqi_str = f'{aqi_info["area"]}區域 ' \
                  f'{predict_time} 預測 {target_time}日\n' \
                  f'AQI：{aqi_info["AQI"]}\n狀況：{aqi_info["status"]}\n' \
                  f'主要污染源：{aqi_info["major_pollutant"]}'
        return [TextSendMessage(text=aqi_str)]
    if '空品現況 ' in msg:
        location = msg_list[1].replace('台', '臺')
        area_list = query_area(location)
        if not area_list:
            return [TextSendMessage(text='查無資料')]
        county_list = []
        for area in area_list:
            if area[1] not in county_list:
                county_list.append(area[1])
        if len(county_list) > 1:
            return [TextSendMessage(text=f'指定的地區有多個可能，請問你指的是哪個縣市？{county_list}')]

        aqi_infos, publish_ts = predict_AQI.query_aqi(county_list[0])
        if not aqi_infos:
            return [TextSendMessage(text='查無資料')]
        date_hr = datetime.fromtimestamp(publish_ts + 8 * 3600).strftime('%m/%d %H 時')
        reply_messages = [TextSendMessage(text=f'{county_list[0]} {date_hr}')]
        aqi_str = ''
        for aqi_info in aqi_infos:
            aqi_str += f'{aqi_info["site_name"]} AQI：{aqi_info["AQI"]} ' \
                       f'狀況：{aqi_info["status"]} 主要污染源：{aqi_info["pollutant"]} ' \
                       f'PM10：{aqi_info["PM10"]} PM2.5：{aqi_info["PM25"]}\n'
        reply_messages.append(TextSendMessage(text=f'{aqi_str}'))
        return reply_messages
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
                return [TextSendMessage(text=result)]

        elif p['type'] == 'search':
            match = p['cmd'].search(msg)
            if match:
                if p.get('matched_as_arg', False):
                    result = p['function'](match.group(0))
                else:
                    result = p['function']()
                return [TextSendMessage(text=result)]

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
