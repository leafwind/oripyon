import re
import os
import random
import time
import logging
import calendar
from datetime import datetime

from linebot.models import (
    TextSendMessage, ImageSendMessage
)

from app.dice import fortune, tarot, nca, choice, gurulingpo
from app import cwb_weather_predictor, predict_AQI
from app.predict_code_map import PREDICT_CODE_MAP
from app import wtf_reasons
from app.emoji_list import cry_emoji_list
from app.util import get_short_url, get_exchange_rate
from taiwan_area_map.query_area import query_area

# equivalent to:
# fortune_pattern = re.compile(ur'\u904b\u52e2', re.UNICODE)
fortune_pattern = re.compile(r'運勢')
tarot_pattern = re.compile(r'塔羅')
gurulingpo_pattern = re.compile(r'咕嚕靈波')
help_pattern = re.compile(r'oripyon\s?說明')
nca_pattern = re.compile(r'nca')
choice_pattern = re.compile(r"""choice\s?  # choice + 0~1 space
                            \[             # [
                            [^,\[\]]+      # not start with , [, ] (at least once)
                            (,[^,\[\]]+)+  # plus dot (at least once)
                            ]              # ]
                            """, re.VERBOSE | re.IGNORECASE)
pattern_mapping = [
    {
        're_obj': fortune_pattern,
        'type': 'search',
        'function': fortune,
    },
    {
        're_obj': nca_pattern,
        'type': 'search',
        'function': nca,
    },
    {
        're_obj': gurulingpo_pattern,
        'type': 'search',
        'function': gurulingpo
    },
    {
        're_obj': choice_pattern,
        'type': 'search',
        'function': choice,
        'matched_as_arg': True
    }
]

last_msg = {}
replied_time = {}


def common_reply(source_id, msg):
    now = int(time.time())
    msg = msg.lower()
    msg_list = msg.split(' ')
    if help_pattern.search(msg):
        reply = '原始碼請看 https://github.com/leafwind/line_bot'
        return [TextSendMessage(text=reply)]
    if '爛中文' in msg:
        reply = '我覺的台灣人的中文水準以經爛ㄉ很嚴重 大家重來都不重視 因該要在加強 才能越來越利害'
        return [TextSendMessage(text=reply)]
    if '幫qq' in msg:
        reply = f'幫QQ喔 {random.choice(cry_emoji_list)}'
        return [TextSendMessage(text=reply)]
    if '魔法少女' in msg:
        reply = '／人◕ ‿‿ ◕人＼ 僕と契約して、魔法少女になってよ！'
        return [TextSendMessage(text=reply)]
    if '請問為什麼' in msg:
        random.seed(os.urandom(5))
        reply = f'因為{random.choice(wtf_reasons.reasons)}。'
        return [TextSendMessage(text=reply)]
    if msg == '空品':
        image_url = f'https://taqm.epa.gov.tw/taqm/Chart/AqiMap/map2.aspx?lang=tw&ts={int(time.time() * 1000)}'
        short_url = get_short_url(image_url)
        return [TextSendMessage(text=short_url)]
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
    if msg == '天氣':
        image_url = f'https://www.cwb.gov.tw/V7/observe/real/Data/Real_Image.png?dumm={int(time.time())}'
        short_url = get_short_url(image_url)
        return [TextSendMessage(text=short_url)]
    if msg == '即時雨量':
        now = int(time.time())
        target_ts = now - 600  # CWB may delay few minutes, set 10 minutes
        target_ts = target_ts // 1800 * 1800  # truncate to 30 minutes
        target_date = datetime.fromtimestamp(target_ts + 8 * 3600)  # UTC+8
        target_date_str = datetime.strftime(target_date, '%Y-%m-%d_%H%M')
        image_url = f'https://www.cwb.gov.tw/V7/observe/rainfall/Data/{target_date_str}.QZT.jpg'
        short_url = get_short_url(image_url)
        logging.info(image_url)
        return [TextSendMessage(text=short_url)]
    if msg == '雷達':
        now = int(time.time())
        target_ts = now - 600  # CWB may delay few minutes, set 10 minutes
        target_ts = target_ts // 600 * 600  # truncate to 10 minutes
        target_date = datetime.fromtimestamp(target_ts + 8 * 3600)  # UTC+8
        target_date_str = datetime.strftime(target_date, '%Y%m%d%H%M')
        image_url = f'https://www.cwb.gov.tw/V7/observe/radar/Data/HD_Radar/CV1_TW_3600_{target_date_str}.png'
        short_url = get_short_url(image_url)
        logging.info(image_url)
        return [TextSendMessage(text=short_url)]
    if msg == '匯率':
        mapping = get_exchange_rate()
        # {
        #     "USDTWD": {
        #         "UTC": "2019-02-02 10:00:10",
        #         "Exrate": 30.7775
        #     },
        #     "USDJPY": {
        #         "UTC": "2019-02-02 10:00:10",
        #         "Exrate": 109.49484758
        #     },
        # }
        usdtwd_date = datetime.strptime(mapping['USDTWD']['UTC'], '%Y-%m-%d %H:%M:%S')
        usdtwd_ts = calendar.timegm(usdtwd_date.timetuple())
        usdtwd_date_utc8 = datetime.utcfromtimestamp(usdtwd_ts + 8 * 3600)
        reply_usd_twd = f'1USD = {mapping["USDTWD"]["Exrate"]} TWD\n{usdtwd_date_utc8}'
        usdjpy_date = datetime.strptime(mapping['USDJPY']['UTC'], '%Y-%m-%d %H:%M:%S')
        usdjpy_ts = calendar.timegm(usdjpy_date.timetuple())
        usdjpy_date_utc8 = datetime.utcfromtimestamp(usdjpy_ts + 8 * 3600)
        reply_usd_jpy = f'1USD = {mapping["USDJPY"]["Exrate"]} JPY\n{usdjpy_date_utc8}'
        reply_jpy_twd = f'估計匯率\n1JPY = {mapping["USDTWD"]["Exrate"] / mapping["USDJPY"]["Exrate"]} TWD\n' \
                        f'以上匯率僅供參考，與當地銀行將會有所出入'
        return [
            TextSendMessage(text=reply_usd_twd),
            TextSendMessage(text=reply_usd_jpy),
            TextSendMessage(text=reply_jpy_twd)
        ]
    if msg_list[0] == '天氣':
        location = msg_list[1].encode('utf-8').replace('台', '臺')
        predicted_result = cwb_weather_predictor.predict(location)
        predicted_result = predicted_result[0]  # temporary use first result
        aqi_info = predict_AQI.predict_aqi(location)
        # image_url = 'http://www.cwb.gov.tw/V7/symbol/weather/gif/night/{}.gif'.format(predicted_result['Wx'])
        if not predicted_result['success']:
            return [TextSendMessage(text='查無資料')]
        if predicted_result['level'] == 2:
            return_str = '\n'.join([
                '{} {} 時為止：'.format(location.encode('utf-8'), predicted_result['time_str']),
                '{} / {} / {}~{}(°C)'.format(PREDICT_CODE_MAP[predicted_result['Wx']], predicted_result['CI'],
                                             str(predicted_result['MinT']), str(predicted_result['MaxT'])),
                '降雨機率：{}%'.format(str(predicted_result['PoP'])),
            ])
            if aqi_info:
                return_str += '\n' + \
                              '{} AQI: {}({} {}) {}預測{}'.format(
                                  aqi_info['area'].encode('utf-8'),
                                  aqi_info['AQI'], aqi_info['major_pollutant'].encode('utf-8'), aqi_info['status'],
                                  datetime.fromtimestamp(aqi_info['publish_ts'] + 8 * 3600).strftime('%m/%d %H'),
                                  datetime.fromtimestamp(aqi_info['forecast_ts'] + 8 * 3600).strftime('%m/%d'),
                              )
        elif predicted_result['level'] == 3:
            return_str = '\n'.join([
                '{} {} 時為止：'.format(location.encode('utf-8'), predicted_result['time_str']),
                '{} / {}°C (體感 {})'.format(PREDICT_CODE_MAP[predicted_result['Wx']], str(predicted_result['T']),
                                           str(predicted_result['AT'])),
                # predicted_result['CI'],
                # '降雨機率：{}%'.format(str(predicted_result['PoP'])),
            ])
            if aqi_info:
                return_str += '\n' + \
                              '{} AQI: {}({} {}) {}預測{}'.format(
                                  aqi_info['area'].encode('utf-8'),
                                  aqi_info['AQI'], aqi_info['major_pollutant'].encode('utf-8'), aqi_info['status'],
                                  datetime.fromtimestamp(aqi_info['publish_ts'] + 8 * 3600).strftime('%m/%d %H'),
                                  datetime.fromtimestamp(aqi_info['forecast_ts'] + 8 * 3600).strftime('%m/%d'),
                              )
        else:
            return [TextSendMessage(text='查無資料')]
        reply = return_str
        return [TextSendMessage(text=reply)]
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
            pass
        elif p['type'] == 'search':
            match = p['re_obj'].search(msg)
            if not match:
                continue
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
