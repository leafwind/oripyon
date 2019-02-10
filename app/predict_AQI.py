import logging
import time

import sqlite3

from constants import CWB_DB_PATH, TABLE_AQI
from taiwan_area_map.query_area import query_area
from app.predict_code_map import AQI_THRESHOLD, AQI_STR

logging.basicConfig(level=logging.DEBUG)

def predict_AQI(location):
    now_ts = int(time.time())
    conn = sqlite3.connect(CWB_DB_PATH)
    area = query_area(location)
    r_dict = {}
    if len(area) == 1:
        area = area[0][0]
        c = conn.cursor()
        query_str = '''SELECT publish_ts, forecast_ts, area, major_pollutant, AQI FROM {} WHERE area=? AND publish_ts = (SELECT MAX(publish_ts) FROM {} WHERE area=?) AND forecast_ts > ? ORDER BY forecast_ts ASC; '''.format(TABLE_AQI, TABLE_AQI)
        c.execute(query_str, (area, area, now_ts - 12 * 3600))
        logging.debug(query_str)
        logging.debug('area: %s, forecast_ts: %s', area, now_ts - 12 * 3600)
        result = c.fetchone()
        publish_ts, forecast_ts, area, major_pollutant, AQI = result
        for i, t in enumerate(AQI_THRESHOLD):
            if AQI + 1 >= t:
                status = AQI_STR[i]
        r_dict = {
            'publish_ts': publish_ts,
            'forecast_ts': forecast_ts,
            'area': area,
            'major_pollutant': major_pollutant,
            'AQI': AQI,
            'status': status,
        }
                
    conn.close()
    return r_dict
