import logging
import time
from datetime import datetime
from app.util import get_short_url


def weather_now():
    image_url = f'https://www.cwb.gov.tw/V7/observe/real/Data/Real_Image.png?dumm={int(time.time())}'
    short_url = get_short_url(image_url)
    return short_url


def rainfall_now():
    now = int(time.time())
    target_ts = now - 600  # CWB may delay few minutes, set 10 minutes
    target_ts = target_ts // 1800 * 1800  # truncate to 30 minutes
    target_date = datetime.fromtimestamp(target_ts + 8 * 3600)  # UTC+8
    target_date_str = datetime.strftime(target_date, '%Y-%m-%d_%H%M')
    image_url = f'https://www.cwb.gov.tw/V7/observe/rainfall/Data/{target_date_str}.QZT.jpg'
    short_url = get_short_url(image_url)
    logging.info(image_url)
    return short_url


def radar_now():
    now = int(time.time())
    target_ts = now - 600  # CWB may delay few minutes, set 10 minutes
    target_ts = target_ts // 600 * 600  # truncate to 10 minutes
    target_date = datetime.fromtimestamp(target_ts + 8 * 3600)  # UTC+8
    target_date_str = datetime.strftime(target_date, '%Y%m%d%H%M')
    image_url = f'https://www.cwb.gov.tw/V7/observe/radar/Data/HD_Radar/CV1_TW_3600_{target_date_str}.png'
    short_url = get_short_url(image_url)
    logging.info(image_url)
    return short_url


def aqi_now():
    image_url = f'https://taqm.epa.gov.tw/taqm/Chart/AqiMap/map2.aspx?lang=tw&ts={int(time.time() * 1000)}'
    short_url = get_short_url(image_url)
    return short_url


def weather():
    # deprecated function
    pass
    '''
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
    '''