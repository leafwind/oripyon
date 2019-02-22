# 引入 requests 模組
import requests
import threading
import time
import json
from line_auth_key import TWITCH_TOKEN, LINE_NOTIFY_OUTH

# 查詢參數
channel_names = {'login': 'MRLO_TW,harnaisxsumire666'}
channel_id = {'channel': '127357428,124941582'} #MrLo_tw,harnaisxsumire666
# 自訂表頭
twitch_headers = {"Client-ID":TWITCH_TOKEN,"Accept": "application/vnd.twitchtv.v5+json"}

line_notify_headers= {'Authorization': 'Bearer ' + LINE_NOTIFY_OUTH,"content-type":'application/x-www-form-urlencoded'}

def mrlo_notify(info):
    my_data = {'message':f"隔壁的 MrLo 開台囉!!\n頻道: https://www.twitch.tv/mrlo_tw\n今日標題:{info['status']}\n分類: {info['game']}",
            'imageThumbnail':'https://i.imgur.com/jWiwOJe.png',
            'imageFullsize':'https://i.imgur.com/jWiwOJe.png'
    }
    requests.post('https://notify-api.line.me/api/notify', headers = line_notify_headers, data = my_data)
    return 

def mao_notify(info):
    my_data = {'message':f"魔王城大炎上的魔王開台囉!!\n頻道: https://www.twitch.tv/harnaisxsumire666\n今日標題:{info['status']}\n分類: {info['game']}",
            'imageThumbnail':'https://i.imgur.com/jWiwOJe.png',
            'imageFullsize':'https://i.imgur.com/jWiwOJe.png'
    }
    requests.post('https://notify-api.line.me/api/notify', headers = line_notify_headers, data = my_data)
    return 

notify_mapping = {
    127357428: {
        'name': 'MrLo_tw',
        'function': mrlo_notify,
    },
    124941582: {
        'name': 'harnaisxsumire666',
        'function': mao_notify,
    }
}

stream_set = set()
def twitch_stream_notify():
    global stream_set
    #r = requests.get('https://api.twitch.tv/kraken/users', headers = twitch_headers, params = channel_names) #get channel ID
    r = requests.get('https://api.twitch.tv/kraken/streams', headers = twitch_headers, params = channel_id) 
    payload = json.loads(r.text)
    new_stream_set = set()
    if payload['_total']>0:
        for streamer in payload['streams']:
            info = streamer['channel']
            id = info['_id']
            new_stream_set.add(id)
            if id not in stream_set:
                notify_mapping[id]['function'](info)
                print(f"{info['display_name']} is streaming")
    stream_set = new_stream_set
class Streamlister:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while self._running:
            twitch_stream_notify();
            time.sleep(15);
        
if __name__ == "__main__":
    try:
        s = Streamlister()
        t = threading.Thread(target=s.run)
        t.start()
        while True:
            time.sleep(0.5)
    except Exception:
        print('exception happened...')
    finally:
        print("exit")
        s.terminate() # Signal termination
        t.join()         