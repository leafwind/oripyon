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

from app.dice import fortune, tarot
from app import cwb_weather_predictor, predict_AQI
from app.predict_code_map import PREDICT_CODE_MAP
from app import wtf_reasons
from app.emoji_list import cry_emoji_list
from app.util import get_short_url, get_exchange_rate
from taiwan_area_map.query_area import query_area

# equivalent to:
# fortune_pattern = re.compile(ur'\u904b\u52e2', re.UNICODE)
fortune_pattern = re.compile('運勢')
tarot_pattern = re.compile('塔羅')
gurulingpo_pattern = re.compile('咕嚕靈波')
help_pattern = re.compile('oripyon\s?說明')
gurulingpo = '''
*``･*+。
 ｜   `*｡
 ｜     *｡
 ｡∩∧ ∧   *
+   (･∀･ )*｡+ﾟ咕嚕靈波
`*｡ ヽ  つ*ﾟ*
 `･+｡*･`ﾟ⊃ +ﾟ
 ☆  ∪~ ｡*ﾟ
 `･+｡*･+ ﾟ
'''


def common_reply(msg):
    msg = msg.lower()
    msg_list = msg.split(' ')
    if help_pattern.search(msg):
        reply = '原始碼請看 https://github.com/leafwind/line_bot'
        return [TextSendMessage(text=reply)]
    if '爛中文' in msg:
        reply = '我覺的台灣人的中文水準以經爛ㄉ很嚴重 大家重來都不重視 因該要在加強 才能越來越利害'
        return [TextSendMessage(text=reply)]
    if '幫qq' in msg:
        reply = '幫QQ喔 {}'.format(random.choice(cry_emoji_list))
        return [TextSendMessage(text=reply)]
    if '魔法少女' in msg:
        reply = '／人◕ ‿‿ ◕人＼ 僕と契約して、魔法少女になってよ！'
        return [TextSendMessage(text=reply)]
    if '請問為什麼' in msg:
        random.seed(os.urandom(5))
        reply = '因為{}。'.format(random.choice(wtf_reasons.reasons))
        return [TextSendMessage(text=reply)]
    if msg == '空品':
        image_url = 'https://taqm.epa.gov.tw/taqm/Chart/AqiMap/map2.aspx?lang=tw&ts={}'.format(
            int(time.time() * 1000)
        )
        short_url = get_short_url(image_url)
        return [TextSendMessage(text=short_url)]
    if '空品預測 ' in msg:
        location = msg_list[1].replace('台', '臺')
        aqi_info = predict_AQI.predict_aqi(location)
        if not aqi_info:
            return [TextSendMessage(text='查無資料')]

        aqi_str = '{}區域 {} 預測 {}日\nAQI：{}\n狀況：{}\n主要污染源：{}'.format(
            aqi_info['area'],
            datetime.fromtimestamp(aqi_info['publish_ts'] + 8 * 3600).strftime('%m/%d %H 時'),
            datetime.fromtimestamp(aqi_info['forecast_ts'] + 8 * 3600).strftime('%m/%d'),
            aqi_info['AQI'], aqi_info['status'], aqi_info['major_pollutant'],
        )
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
            return [TextSendMessage(text='指定的地區有多個可能，請問你指的是哪個縣市？{}'.format(county_list))]#

        aqi_infos, publish_ts = predict_AQI.query_aqi(county_list[0])
        if not aqi_infos:
            return [TextSendMessage(text='查無資料')]
        reply_messages = []
        reply_messages.append(TextSendMessage(
            text='{county} {date_hr}'.format(
                county=county_list[0],
                date_hr=datetime.fromtimestamp(publish_ts + 8 * 3600).strftime('%m/%d %H 時'),
            )
        ))
        aqi_str = ''
        for aqi_info in aqi_infos:
            aqi_str += '{site_name} AQI：{aqi} 狀況：{status} 主要污染源：{pollutant} PM10：{PM10} PM2.5：{PM25}\n'.format(
                site_name=aqi_info['site_name'],
                aqi=aqi_info['AQI'],
                pollutant=aqi_info['pollutant'],
                status=aqi_info['status'],
                PM10=aqi_info['PM10'],
                PM25=aqi_info['PM25'],
            )
        reply_messages.append(TextSendMessage(text='{}'.format(aqi_str)))
        return reply_messages
    if msg == '天氣':
        image_url = 'https://www.cwb.gov.tw/V7/observe/real/Data/Real_Image.png?dumm={}'.format(
            int(time.time())
        )
        short_url = get_short_url(image_url)
        return [TextSendMessage(text=short_url)]
    if msg == '即時雨量':
        now = int(time.time())
        target_ts = now - 600  # CWB may delay few minutes, set 10 minutes
        target_ts = target_ts // 1800 * 1800  # truncate to 30 minutes
        target_date = datetime.fromtimestamp(target_ts + 8 * 3600)  # UTC+8
        image_url = 'https://www.cwb.gov.tw/V7/observe/rainfall/Data/{}.QZT.jpg'.format(
            datetime.strftime(target_date, '%Y-%m-%d_%H%M')
        )
        short_url = get_short_url(image_url)
        logging.info(image_url)
        return [TextSendMessage(text=short_url)]
    if msg == '雷達':
        now = int(time.time())
        target_ts = now - 600  # CWB may delay few minutes, set 10 minutes
        target_ts = target_ts // 600 * 600  # truncate to 10 minutes
        target_date = datetime.fromtimestamp(target_ts + 8 * 3600)  # UTC+8
        image_url = 'https://www.cwb.gov.tw/V7/observe/radar/Data/HD_Radar/CV1_TW_3600_{}.png'.format(
            datetime.strftime(target_date, '%Y%m%d%H%M')
        )
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
        reply_usd_twd = '1USD = {} TWD\n{}'.format(
            mapping['USDTWD']['Exrate'],
            usdtwd_date_utc8
        )
        usdjpy_date = datetime.strptime(mapping['USDJPY']['UTC'], '%Y-%m-%d %H:%M:%S')
        usdjpy_ts = calendar.timegm(usdjpy_date.timetuple())
        usdjpy_date_utc8 = datetime.utcfromtimestamp(usdjpy_ts + 8 * 3600)
        reply_usd_jpy = '1USD = {} JPY\n{}'.format(
            mapping['USDJPY']['Exrate'],
            usdjpy_date_utc8
        )
        reply_jpy_twd = '估計匯率\n1JPY = {} TWD\n以上匯率僅供參考，與當地銀行將會有所出入'.format(
            mapping['USDTWD']['Exrate'] / mapping['USDJPY']['Exrate'],
        )
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
    if gurulingpo_pattern.search(msg):
        return [TextSendMessage(text=gurulingpo)]
    if tarot_pattern.search(msg):
        card = tarot()
        image_message = ImageSendMessage(
            original_content_url=card['url'],
            preview_image_url=card['url']
        )
        return [
            image_message,
            TextSendMessage(text='{}: {}'.format(card['nameCN'], card['conclusion']))
        ]
    elif fortune_pattern.search(msg):
        result = fortune()
        return [TextSendMessage(text=result)]
    else:
        return []
