# -*- coding: utf-8 -*-

import re
import os
import random
import time
import logging
from datetime import datetime

from linebot.models import (
    TextSendMessage, ImageSendMessage
)

from dice import fortune, tarot
from app import cwb_weather_predictor, predict_AQI
from predict_code_map import PREDICT_CODE_MAP
from app import wtf_reasons

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


def common_reply(msg, line_bot_api, _source_id, reply_token):
    msg_list = msg.split(' ')
    if help_pattern.search(msg):
        reply = '原始碼請看 https://github.com/leafwind/line_bot'
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=reply)])
        return True
    if '爛中文' in msg:
        reply = '我覺的台灣人的中文水準以經爛ㄉ很嚴重 大家重來都不重視 因該要在加強 才能越來越利害'
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=reply)])
        return True
    if '幫QQ' in msg:
        reply = '幫QQ喔'
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=reply)])
        return True
    if '魔法少女' in msg:
        reply = '僕と契約して、魔法少女になってよ！'
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=reply)])
        return True
    if '請問為什麼' in msg:
        random.seed(os.urandom(5))
        reply = '因為{}。'.format(random.choice(wtf_reasons.reasons))
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=reply)])
        return True
    if msg == '空品':
        image_url = 'https://taqm.epa.gov.tw/taqm/Chart/AqiMap/map2.aspx?lang=tw&ts={}'.format(
            int(time.time() * 1000)
        )
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        line_bot_api.reply_message(reply_token, [
            image_message,
        ])
        return True
    if msg == '天氣':
        image_url = 'https://www.cwb.gov.tw/V7/observe/real/Data/Real_Image.png?dumm={}'.format(
            int(time.time())
        )
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        line_bot_api.reply_message(reply_token, [
            image_message,
        ])
        return True
    if msg == '即時雨量':
        now = int(time.time())
        target_ts = now - 600  # CWB may delay few minutes, set 10 minutes
        target_ts = target_ts / 1800 * 1800  # truncate to 30 minutes
        target_date = datetime.fromtimestamp(target_ts + 8 * 3600)  # UTC+8
        image_url = 'https://www.cwb.gov.tw/V7/observe/rainfall/Data/{}.QZT.jpg'.format(
            datetime.strftime(target_date, '%Y-%m-%d_%H%M')
        )
        logging.info(image_url)
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        line_bot_api.reply_message(reply_token, [
            image_message,
        ])
        return True
    if msg == '雷達':
        now = int(time.time())
        target_ts = now - 600  # CWB may delay few minutes, set 10 minutes
        target_ts = target_ts / 1800 * 1800  # truncate to 30 minutes
        target_date = datetime.fromtimestamp(target_ts + 8 * 3600)  # UTC+8
        image_url = 'https://www.cwb.gov.tw/V7/observe/radar/Data/HD_Radar/CV1_TW_3600_{}.png'.format(
            datetime.strftime(target_date, '%Y%m%d%H%M')
        )
        logging.info(image_url)
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        line_bot_api.reply_message(reply_token, [
            image_message,
        ])
        return True
    if msg_list[0] == '天氣':
        location = msg_list[1].encode('utf-8').replace('台', '臺')
        predicted_result = cwb_weather_predictor.predict(location)
        predicted_result = predicted_result[0]  # temporary use first result
        AQI = predict_AQI.predict_AQI(location)
        # image_url = 'http://www.cwb.gov.tw/V7/symbol/weather/gif/night/{}.gif'.format(predicted_result['Wx'])
        if not predicted_result['success']:
            return '查無資料'
        if predicted_result['level'] == 2:
            return_str = '\n'.join([
                '{} {} 時為止：'.format(location.encode('utf-8'), predicted_result['time_str']),
                '{} / {} / {}~{}(°C)'.format(PREDICT_CODE_MAP[predicted_result['Wx']], predicted_result['CI'],
                                             str(predicted_result['MinT']), str(predicted_result['MaxT'])),
                '降雨機率：{}%'.format(str(predicted_result['PoP'])),
            ])
            if AQI:
                return_str += '\n' + \
                              '{} AQI: {}({} {}) {}預測{}'.format(
                                  AQI['area'].encode('utf-8'),
                                  AQI['AQI'], AQI['major_pollutant'].encode('utf-8'), AQI['status'],
                                  datetime.fromtimestamp(AQI['publish_ts'] + 8 * 3600).strftime('%m/%d %H'),
                                  datetime.fromtimestamp(AQI['forecast_ts'] + 8 * 3600).strftime('%m/%d'),
                              )
        elif predicted_result['level'] == 3:
            return_str = '\n'.join([
                '{} {} 時為止：'.format(location.encode('utf-8'), predicted_result['time_str']),
                '{} / {}°C (體感 {})'.format(PREDICT_CODE_MAP[predicted_result['Wx']], str(predicted_result['T']),
                                           str(predicted_result['AT'])),
                # predicted_result['CI'],
                # '降雨機率：{}%'.format(str(predicted_result['PoP'])),
            ])
            if AQI:
                return_str += '\n' + \
                              '{} AQI: {}({} {}) {}預測{}'.format(
                                  AQI['area'].encode('utf-8'),
                                  AQI['AQI'], AQI['major_pollutant'].encode('utf-8'), AQI['status'],
                                  datetime.fromtimestamp(AQI['publish_ts'] + 8 * 3600).strftime('%m/%d %H'),
                                  datetime.fromtimestamp(AQI['forecast_ts'] + 8 * 3600).strftime('%m/%d'),
                              )
        else:
            return '查無資料'
        reply = return_str
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=reply)])
        return True
    if gurulingpo_pattern.search(msg):
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=gurulingpo)
        ])
        return True
    if tarot_pattern.search(msg):
        card = tarot()
        image_message = ImageSendMessage(
            original_content_url=card['url'],
            preview_image_url=card['url']
        )
        line_bot_api.reply_message(reply_token, [
            image_message,
            TextSendMessage(text='{}: {}'.format(card['nameCN'].encode('utf-8'), card['conclusion'].encode('utf-8')))
        ])
        return True
    elif fortune_pattern.search(msg):
        result = fortune()
        line_bot_api.reply_message(reply_token, [
            TextSendMessage(text=result)
        ])
        return True
    else:
        return False
