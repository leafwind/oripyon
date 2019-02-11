import logging
import time

import sqlite3

from constants import CWB_DB_PATH, TABLE_AQFN, TABLE_AQI
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
    query_str = '''SELECT publish_ts, forecast_ts, area, major_pollutant, AQI FROM {} WHERE area=? AND publish_ts = (SELECT MAX(publish_ts) FROM {} WHERE area=?) AND forecast_ts > ? ORDER BY forecast_ts ASC; '''.format(
        TABLE_AQFN, TABLE_AQFN)
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


def query_aqi(county):
    conn = sqlite3.connect(CWB_DB_PATH)
    c = conn.cursor()

    query_str = '''SELECT MAX(publish_ts) FROM {TABLE_AQI} WHERE county=?; '''.format(
        TABLE_AQI=TABLE_AQI)
    logging.debug(query_str)
    logging.debug('county: %s', county)
    c.execute(query_str, [county])
    publish_ts = c.fetchone()

    query_str = '''SELECT site_name, publish_ts, AQI, pollutant, status, PM10, PM25 FROM {TABLE_AQI} WHERE county=? AND publish_ts = ?; '''.format(
        TABLE_AQI=TABLE_AQI)
    logging.debug(query_str)
    logging.debug('county: %s, publish_ts: %s', county, publish_ts)
    c.execute(query_str, (county, publish_ts))
    result = c.fetchall()
    r_list = []
    for r in result:
        site_name, publish_ts, AQI, pollutant, status, PM10, PM25 = r
        r_list.append({
            'county': county,
            'site_name': site_name,
            'AQI': AQI,
            'pollutant': pollutant if pollutant else '無',
            'status': status,
            'PM10': PM10,
            'PM25': PM25,
        })

    conn.close()
    return r_list, publish_ts
