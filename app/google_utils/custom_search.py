import json
import logging
import random
import os

import requests

from constants import GOOGLE_API_KEY_PATH

with open(GOOGLE_API_KEY_PATH, 'r') as _f:
    data = json.load(_f)
    API_KEY = data['API_KEY']

def get_google_custom_search_result(query_string, num=10, search_type='image'):
    global API_KEY
    api_url = 'https://www.googleapis.com/customsearch/v1'
    api_url += f'?key={API_KEY}'
    api_url += f'&num={num}'
    api_url += f'&searchType={search_type}'
    api_url += f'&q={query_string}'
    api_url += f'&cx=013563099022526892869:vdjdigrv2sm'
    logging.info(api_url)
    r = requests.get(api_url)
    items = r.json()['items']
    images = [(i['title'], i['link']) for i in items if i['link'].startswith('https')]
    if r.status_code == 200:
        return images
    else:
        logging.error(r.status_code)


def google_search_image(msg):
    msg = " ".join(msg.split())
    query = msg.split(' ')[1]
    random.seed(os.urandom(5))
    images = get_google_custom_search_result(query)
    image = random.choice(images)
    replies = [('image', image[1]), ('text', image[0])]
    return replies