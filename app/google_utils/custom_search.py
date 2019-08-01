import json
import logging
import random
import os

import requests

from constants import GOOGLE_API_KEY_PATH

with open(GOOGLE_API_KEY_PATH, 'r') as _f:
    data = json.load(_f)
    API_KEY = data['API_KEY']


def get_google_custom_search_result(query_string, num=10, safe='active', search_type='image'):
    global API_KEY
    api_url = 'https://www.googleapis.com/customsearch/v1'
    api_url += f'?key={API_KEY}'
    api_url += f'&num={num}'
    api_url += f'&safe={safe}'
    api_url += f'&searchType={search_type}'
    api_url += f'&q={query_string}'
    api_url += f'&cx=013563099022526892869:vdjdigrv2sm'
    logging.info(api_url)
    r = requests.get(api_url)
    result = r.json()
    if 'items' in result:
        images = [(i['title'], i['link']) for i in result['items'] if i['link'].startswith('https')]
        return images
    elif 'error' in result:
        if 'errors' in result['error']:
            if 'reason' in result['error']['errors'][0]:
                if result['error']['errors'][0]['reason'] == 'dailyLimitExceeded':
                    images = [('Google 一天一百次免費用完了...QQ', 'https://i.imgur.com/bvNKRTz.jpg')]
                    return images
        else:
            images = [('發生某種問題QQ', 'https://i.imgur.com/kqfL1bN.jpg')]
            logging.error(result)
            return images
    images = [('發生某種問題QQ', 'https://i.imgur.com/kqfL1bN.jpg')]
    logging.error(result)
    return images


def google_search_image(msg):
    msg = " ".join(msg.split())
    query = msg.split(' ')[1]
    random.seed(os.urandom(5))
    images = get_google_custom_search_result(query)
    image = random.choice(images)
    replies = [('image', image[1]), ('text', image[0])]
    return replies