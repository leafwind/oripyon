import logging
import time
from datetime import datetime
from app.util import get_short_url, get_reservoir_stat
from app import predict_AQI
from taiwan_area_map.query_area import query_area


def reservoir_now():
    reservoir_stat = get_reservoir_stat()
    replies = []
    for reservoir_name in ['翡翠水庫', '石門水庫']:
        r = reservoir_stat[reservoir_name]
        total = float(r['baseAvailable'])
        updated_at = r['updateAt']
        percentage = r['percentage']
        diff = r['daliyNetflow']
        diff_percentage = diff / total
        estimated_remain_days = percentage // (diff / total)
        up_or_down = '上升' if diff < 0 else '下降'
        replies.append((
            'text', f'{reservoir_name} 百分比：{percentage}\n'
                f'昨日水量{up_or_down}：{diff_percentage}% 預測剩餘天數：{estimated_remain_days}天 \n'
                f'更新時間：{updated_at}'
        ))
    replies.append(('text', '其他水庫資訊請參考 https://water.taiwanstat.com/'))
    return replies


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


def aqi_predict(msg):
    msg_list = msg.split(' ')
    location = msg_list[1].replace('台', '臺')
    aqi_info = predict_AQI.predict_aqi(location)
    if not aqi_info:
        return '查無資料'

    predict_time = datetime.fromtimestamp(aqi_info['publish_ts'] + 8 * 3600).strftime('%m/%d %H 時')
    target_time = datetime.fromtimestamp(aqi_info['forecast_ts'] + 8 * 3600).strftime('%m/%d')
    aqi_str = f'{aqi_info["area"]}區域 ' \
              f'{predict_time} 預測 {target_time}日\n' \
              f'AQI：{aqi_info["AQI"]}\n狀況：{aqi_info["status"]}\n' \
              f'主要污染源：{aqi_info["major_pollutant"]}'
    return aqi_str


def aqi_status(msg):
    msg_list = msg.split(' ')
    location = msg_list[1].replace('台', '臺')
    area_list = query_area(location)
    if not area_list:
        return [('text', '查無資料')]
    county_list = []
    for area in area_list:
        if area[1] not in county_list:
            county_list.append(area[1])
    if len(county_list) > 1:
        return [('text', f'指定的地區有多個可能，請問你指的是哪個縣市？{county_list}')]

    aqi_infos, publish_ts = predict_AQI.query_aqi(county_list[0])
    if not aqi_infos:
        return [('text', '查無資料')]
    date_hr = datetime.fromtimestamp(publish_ts + 8 * 3600).strftime('%m/%d %H 時')
    reply_messages = [('text', f'{county_list[0]} {date_hr}')]
    aqi_str = ''
    for aqi_info in aqi_infos:
        aqi_str += f'{aqi_info["site_name"]} AQI：{aqi_info["AQI"]} ' \
                   f'狀況：{aqi_info["status"]} 主要污染源：{aqi_info["pollutant"]} ' \
                   f'PM10：{aqi_info["PM10"]} PM2.5：{aqi_info["PM25"]}\n'
    reply_messages.append(('text', f'{aqi_str}'))
    return reply_messages


def weather():
    # deprecated function
    pass
    '''
    from app.predict_code_map import PREDICT_CODE_MAP
    from app import cwb_weather_predictor
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