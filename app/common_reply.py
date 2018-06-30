# -*- coding: utf-8 -*-

import re
from datetime import datetime

from linebot.models import (
    TextSendMessage, ImageSendMessage
)

from dice import fortune, tarot
from app import cwb_weather_predictor, predict_AQI
from predict_code_map import PREDICT_CODE_MAP

# equivalent to:
# fortune_pattern = re.compile(ur'\u904b\u52e2', re.UNICODE)
fortune_pattern = re.compile('運勢'.decode('utf-8'))
tarot_pattern = re.compile('塔羅'.decode('utf-8'))
help_pattern = re.compile('oripyon\s?說明'.decode('utf-8'))

def common_reply(msg, line_bot_api, source_id, reply_token):
    msg_list = msg.split(' ')
    if help_pattern.search(msg):
        reply = '原始碼請看 https://github.com/leafwind/line_bot'
        line_bot_api.reply_message(reply_token, [ TextSendMessage(text=reply) ])
        return True
    if '爛中文'.decode('utf-8') in msg:
        reply = '我覺的台灣人的中文水準以經爛ㄉ很嚴重 大家重來都不重視 因該要在加強 才能越來越利害'
        line_bot_api.reply_message(reply_token, [ TextSendMessage(text=reply) ])
        return True
    if msg_list[0] == '天氣'.decode('utf-8'):
        location = msg_list[1].encode('utf-8').replace('台', '臺').decode('utf-8')
        predicted_result = cwb_weather_predictor.predict(location)
        predicted_result = predicted_result[0]  # temporary use first result
        AQI = predict_AQI.predict_AQI(location)
        # image_url = 'http://www.cwb.gov.tw/V7/symbol/weather/gif/night/{}.gif'.format(predicted_result['Wx'])
        if not predicted_result['success']:
            return '查無資料'
        if predicted_result['level'] == 2:
            return_str = '\n'.join([
                '{} {} 時為止：'.format(location.encode('utf-8'), predicted_result['time_str']),
                '{} / {} / {}~{}(°C)'.format(PREDICT_CODE_MAP[predicted_result['Wx']], predicted_result['CI'], str(predicted_result['MinT']), str(predicted_result['MaxT'])),
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
                '{} / {}°C (體感 {})'.format(PREDICT_CODE_MAP[predicted_result['Wx']], str(predicted_result['T']), str(predicted_result['AT'])),
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
        reply = return_str
        line_bot_api.reply_message(reply_token, [ TextSendMessage(text=reply) ])
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
