import logging
import time

import sqlite3

from constants import CWB_DB_PATH, TABLE_AQI
from taiwan_area_map.query_area import query_area
from app.predict_code_map import AQI_THRESHOLD, AQI_STR

logging.basicConfig(level=logging.DEBUG)


def get_aqi_status_str(aqi):
    status = '良好'
    for i, t in enumerate(AQI_THRESHOLD):
        if aqi + 1 >= t:
            status = AQI_STR[i]
    return status


def predict_aqi(location):
    now_ts = int(time.time())
    conn = sqlite3.connect(CWB_DB_PATH)
    area_list = query_area(location)

    if not area_list:
        return {}
    if len(area_list) >= 2:
        # multi-match, choose first as the area
        area_list = area_list[:1]

    area_list = area_list[0][0]
    c = conn.cursor()
    query_str = '''SELECT publish_ts, forecast_ts, area, major_pollutant, AQI FROM {} WHERE area=? AND publish_ts = (SELECT MAX(publish_ts) FROM {} WHERE area=?) AND forecast_ts > ? ORDER BY forecast_ts ASC; '''.format(TABLE_AQI, TABLE_AQI)
    c.execute(query_str, (area_list, area_list, now_ts - 12 * 3600))
    logging.debug(query_str)
    logging.debug('area: %s, forecast_ts: %s', area_list, now_ts - 12 * 3600)
    result = c.fetchone()
    publish_ts, forecast_ts, area_list, major_pollutant, aqi = result

    r_dict = {
        'publish_ts': publish_ts,
        'forecast_ts': forecast_ts,
        'area': area_list,
        'major_pollutant': major_pollutant if major_pollutant else '無',
        'AQI': aqi,
        'status': get_aqi_status_str(aqi),
    }
                
    conn.close()
    return r_dict
