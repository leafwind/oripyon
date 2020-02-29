import logging

import requests


def get_short_url(target_url):
    test_access_token = '20f07f91f3303b2f66ab6f61698d977d69b83d64'
    api_url = 'https://api.pics.ee/v1/links/?access_token={}'.format(test_access_token)
    r = requests.post(api_url, data={"url": target_url})
    if r.status_code == 200:
        return r.json()['data']['picseeUrl']
    else:
        logging.getLogger(__name__).error(r.status_code)


def get_exchange_rate():
    r = requests.get('https://tw.rter.info/capi.php')
    mapping = r.json()
    return mapping


def get_like_eth_liquid():
    r = requests.get('https://api.liquid.com/products')
    result = r.json
    like_eth = result[210]
    name = like_eth['currency_pair_code']
    volume = like_eth["volume_24h"]
    last_price = like_eth["last_price_24h"]
    ts = like_eth["last_event_timestamp"]
    ts = int(float(ts))
    return name, volume, last_price, ts


def get_like_coinmarketcap():
    r = requests.get('https://graphs2.coinmarketcap.com/currencies/likecoin/')
    result = r.json()
    [timestamp_ms, price] = result['price_usd'][-1]
    return timestamp_ms, price


def get_reservoir_stat():
    r = requests.get('https://www.taiwanstat.com/waters/latest')
    return r.json()[0]
