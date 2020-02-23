import json
import logging
import random
import os

import requests

from constants import GOOGLE_API_KEY_PATH

with open(GOOGLE_API_KEY_PATH, 'r') as _f:
    data = json.load(_f)
    API_KEY = data['API_KEY']

# CSE setting
# https://cse.google.com/cse/setup/basic?cx=010322789978293582519:tmzyqrdufxq
# google api key
# https://console.developers.google.com/apis/credentials?project=phrasal-ability-235508
# https://developers.google.com/custom-search/v1/using_rest
# https://developers.google.com/custom-search/v1/cse/list


def get_google_custom_search_result(query_string, num=10, safe='active', search_type='image'):
    global API_KEY
    api_url = 'https://www.googleapis.com/customsearch/v1'
    api_url += f'?key={API_KEY}'
    api_url += f'&num={num}'
    api_url += f'&safe={safe}'
    api_url += f'&searchType={search_type}'
    api_url += f'&q={query_string}'
    api_url += f'&cx=010322789978293582519:tmzyqrdufxq'
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


def google_search_image(msg, msg_info, _robot_settings):
    allow_google_search_group_ids = [
        'C1bebaeaf89242089f0d755d492df6cb6',  # 測試群組
        'Cfb6a76351d112834244144a1cd4f0f57',  # 死愛魔王城
        'C1e38a92f8c7b4ad377df882b9f3bf336',  # 尼爾主題餐廳
        'Cbc420349e56f3bae5d5f46fafb0ac5cb',  # 社畜人生的煩惱
        'Cf794cf7dc1970c3fba9122673cf3dcde',  # 魔王城測試
    ]
    if msg_info.source_id not in allow_google_search_group_ids:
        return []
    msg = " ".join(msg.split())
    query = msg.split(' ')[1]
    random.seed(os.urandom(5))
    images = get_google_custom_search_result(query)
    image = random.choice(images)
    replies = [('image', image[1]), ('text', image[0])]
    return replies
