"""
polling twitch api and notify line if streaming online
"""
import threading
import time
import json
import logging

import yaml
import requests


with open("./secret.yml", 'r') as stream:
    _data = yaml.load(stream)
    TWITCH_TOKEN = _data['TWITCH_TOKEN']
    LINE_NOTIFY_SECRET = _data['LINE_NOTIFY_SECRET']

def notify(data):
    """
    :param data:
    :return:
    """
    line_notify_headers = {
        'Authorization': 'Bearer ' + LINE_NOTIFY_SECRET,
        "content-type": 'application/x-www-form-urlencoded'
    }
    requests.post(
        'https://notify-api.line.me/api/notify',
        headers=line_notify_headers, data=data
    )


stream_set = set()
def twitch_stream_notify():
    """
    :return:
    """
    global stream_set
    twitch_headers = {
        "Client-ID": TWITCH_TOKEN,
        "Accept": "application/vnd.twitchtv.v5+json"
    }
    channel_id = {'channel': '127357428,124941582'}  # MrLo_tw, harnaisxsumire666
    r = requests.get(
        'https://api.twitch.tv/kraken/streams',
        headers=twitch_headers,
        params=channel_id
    )

    notify_mapping = {
        127357428: {
            'name': '隔壁的 MrLo',
            'url': 'https://www.twitch.tv/mrlo_tw',
        },
        124941582: {
            'name': '魔王城大炎上的魔王',
            'url': 'https://www.twitch.tv/harnaisxsumire666',
        }
    }
    payload = json.loads(r.text)
    new_stream_set = set()
    if payload['_total'] > 0:
        for streamer in payload['streams']:
            info = streamer['channel']
            twitch_id = info['_id']
            new_stream_set.add(twitch_id)
            if twitch_id not in stream_set:
                data = {
                    'message': f"{notify_mapping[twitch_id]['name']}開台囉!!\n"
                               f"頻道: {notify_mapping[twitch_id]['url']}\n"
                               f"今日標題: {info['status']}\n"
                               f"分類: {info['game']}",
                    'imageThumbnail': 'https://i.imgur.com/jWiwOJe.png',
                    'imageFullsize': 'https://i.imgur.com/jWiwOJe.png'
                }
                notify(data)
                logging.info("%s is streaming", info['display_name'])
    stream_set = new_stream_set


class StreamLister:
    """
    """
    def __init__(self):
        self._running = True

    def terminate(self):
        """
        :return:
        """
        self._running = False

    def run(self):
        """
        :return:
        """
        while self._running:
            twitch_stream_notify()
            time.sleep(15)


if __name__ == "__main__":
    sl = StreamLister()
    t = threading.Thread(target=sl.run)
    try:
        t.start()
        while True:
            time.sleep(0.5)
    except Exception as e:
        logging.exception('exception: %s', e)
    finally:
        logging.info("exit")
        sl.terminate()  # Signal termination
        t.join()
