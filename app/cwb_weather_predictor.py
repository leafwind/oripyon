# -*- coding: utf-8 -*-
import logging
import time
from datetime import datetime

import sqlite3

from constants import CWB_DB_PATH

logging.basicConfig(level=logging.DEBUG)


def predict(location):
    conn = sqlite3.connect(CWB_DB_PATH)
    ts_now = int(time.time())

    c = conn.cursor()
    query_str = '''SELECT end_ts, Wx, MaxT, MinT, PoP, CI FROM {} WHERE location=? AND end_ts > ? ORDER BY end_ts ASC; '''.format('level_1_2')
    c.execute(query_str, (location, ts_now))
    logging.debug(query_str)
    logging.debug(location)
    logging.debug(ts_now)
    result_level_1_2 = c.fetchall()
    if result_level_1_2:
        conn.close()
        return_list = []
        for r in result_level_1_2:
            end_ts, Wx, MaxT, MinT, PoP, CI = r
            data = {
                'success': True,
                'level': 2,
                'end_ts': end_ts,
                'Wx': Wx,
                'MaxT': MaxT,
                'MinT': MinT,
                'PoP': PoP,
                'CI': CI.encode('utf-8'),
                'time_str': datetime.fromtimestamp(end_ts + 8 * 3600).strftime('%m/%d %H')
            }
            return_list.append(data)
    else:
        query_str = '''SELECT start_ts, end_ts, Wx, T, AT, PoP, CI FROM {} WHERE sub_location=? AND start_ts > ? ORDER BY start_ts ASC; '''.format('level_3')
        c.execute(query_str, (location, ts_now))
        logging.debug(query_str)
        logging.debug(location)
        logging.debug(ts_now)
        result_level_3 = c.fetchall()
        # INSERT OR REPLACE INTO level_3 VALUES ('宜蘭縣', '五結鄉', 1489734000, 1489744800, 26, 21, 21, 0, '')
        if not result_level_3:
            conn.close()
            return [{'success': False}]
        return_list = []
        for r in result_level_3:
            start_ts, end_ts, Wx, T, AT, PoP, CI = r
            data = {
                'success': True,
                'level': 3,
                'start_ts': start_ts,
                'end_ts': end_ts,
                'Wx': Wx,
                'T': T,
                'AT': AT,
                'time_str': datetime.fromtimestamp(start_ts + 8 * 3600).strftime('%m/%d %H')
            }
            return_list.append(data)

    return return_list
