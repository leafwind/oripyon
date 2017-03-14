# -*- coding: utf-8 -*-
import logging
import time
from datetime import datetime

import sqlite3

from constants import CWB_DB_PATH

logging.basicConfig(level=logging.DEBUG)

def predict(location):
    ts_now = int(time.time())
    conn = sqlite3.connect(CWB_DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT end_ts, Wx, MaxT, MinT, PoP, CI FROM {} WHERE location=? AND end_ts > ? ORDER BY end_ts ASC; '''.format('forecast_36hr'), (location, ts_now))
    result = c.fetchall()
    if not result:
        return '查無資料'
    conn.close()

    return_list = []
    for r in result:
        end_ts, Wx, MaxT, MinT, PoP, CI = r
        data = {
            'end_ts': end_ts,
            'Wx': Wx,
            'MaxT': MaxT,
            'MinT': MinT,
            'PoP': PoP,
            'CI': CI.encode('utf-8'),
            'time_str': datetime.fromtimestamp(end_ts + 8 * 3600).strftime('%m/%d %H')
        }
        return_list.append(data)

    return return_list
