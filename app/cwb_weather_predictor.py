# -*- coding: utf-8 -*-
import logging
import time
from datetime import datetime

import sqlite3

from constants import CWB_DB_PATH
from predict_code_map import PREDICT_CODE_MAP

logging.basicConfig(level=logging.DEBUG)

def predict(location):
    ts_now = int(time.time())
    conn = sqlite3.connect(CWB_DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT end_ts, Wx, MaxT, MinT, PoP, CI FROM {} WHERE location=? AND end_ts > ? ORDER BY end_ts ASC; '''.format('forecast_36hr'), (location, ts_now))
    result = c.fetchall()
    if not result:
        return '查無資料'
    result = result[0]  # tmp
    end_ts, Wx, MaxT, MinT, PoP, CI = result
    CI = CI.encode('utf-8')
    time_str = datetime.fromtimestamp(end_ts + 8 * 3600).strftime('%m/%d %H')

    conn.close()
    reply = location.encode('utf-8') + ' ' + time_str + '時為止：\n天氣：' + PREDICT_CODE_MAP[Wx] + '\n' + CI + '\n溫度：' + str(MinT) + '~' + str(MaxT) + '(C)\n降雨機率：' + str(PoP) + '%'
    return reply
