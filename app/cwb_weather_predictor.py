# -*- coding: utf-8 -*-
import logging

import sqlite3

from constants import CWB_DB_PATH

logging.basicConfig(level=logging.DEBUG)

def predict(location):
    conn = sqlite3.connect(CWB_DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT end_ts, Wx, MaxT, MinT, PoP, CI FROM {} WHERE location=?; '''.format('forecast_36hr'), (location,))
    result = c.fetchall()
    conn.close()
    if not result:
        return '查無資料'
    print result
    return result[0][5]
