import calendar
from datetime import datetime

from app.util import get_exchange_rate


def exchange_rate(_msg_info, _robot_settings):
    mapping = get_exchange_rate()
    # {
    #     "USDTWD": {
    #         "UTC": "2019-02-02 10:00:10",
    #         "Exrate": 30.7775
    #     },
    #     "USDJPY": {
    #         "UTC": "2019-02-02 10:00:10",
    #         "Exrate": 109.49484758
    #     },
    # }
    usdtwd_date = datetime.strptime(mapping['USDTWD']['UTC'], '%Y-%m-%d %H:%M:%S')
    usdtwd_ts = calendar.timegm(usdtwd_date.timetuple())
    usdtwd_date_utc8 = datetime.utcfromtimestamp(usdtwd_ts + 8 * 3600)
    reply_usd_twd = f'1USD = {mapping["USDTWD"]["Exrate"]} TWD\n{usdtwd_date_utc8}'
    usdjpy_date = datetime.strptime(mapping['USDJPY']['UTC'], '%Y-%m-%d %H:%M:%S')
    usdjpy_ts = calendar.timegm(usdjpy_date.timetuple())
    usdjpy_date_utc8 = datetime.utcfromtimestamp(usdjpy_ts + 8 * 3600)
    reply_usd_jpy = f'1USD = {mapping["USDJPY"]["Exrate"]} JPY\n{usdjpy_date_utc8}'
    reply_jpy_twd = f'估計匯率\n1JPY = {mapping["USDTWD"]["Exrate"] / mapping["USDJPY"]["Exrate"]} TWD'
    comment = f'以上匯率僅供參考，與當地銀行將會有所出入'
    return '\n'.join([reply_usd_twd, reply_usd_jpy, reply_jpy_twd, comment])
