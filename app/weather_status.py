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