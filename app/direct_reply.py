import os
import random
from datetime import datetime, timedelta

import time

from app import wtf_reasons
from app.emoji_list import CRY_EMOJI_LIST


def pier_girl(_msg_info, _robot_settings):
    random.seed(os.urandom(5))
    return random.choice(
        [
            'https://www.youtube.com/watch?v=BoD4yCTXTCU',
            'https://www.youtube.com/watch?v=M-MT0z6ac7g'
        ]
    )


def girlfriend(_msg_info, _robot_settings):
    return [('image', 'https://i.imgur.com/g6WRWrk.jpg')]


def daughter_red(_msg_info, _robot_settings):
    replies = [('image', 'https://i.imgur.com/vKGB3XM.jpg'), ('text', '杜家庄女兒紅 七日釀造 七星獎 口碑88分')]
    return replies


def bot_help(_msg_info, _robot_settings):
    return '說明網頁 https://oripyon.weebly.com\n原始碼 https://github.com/leafwind/line_bot'


def poor_chinese(_msg_info, _robot_settings):
    return '我覺的台灣人的中文水準以經爛ㄉ很嚴重 大家重來都不重視 因該要在加強 才能越來越利害'


def qq(_msg_info, _robot_settings):
    random.seed(os.urandom(5))
    return f'幫QQ喔 {random.choice(CRY_EMOJI_LIST)}'


def mahoshoujo(_msg_info, _robot_settings):
    return '／人◕ ‿‿ ◕人＼ 僕と契約して、魔法少女になってよ！'


def _find_next_boss_time():
    boss_times_interval_from_utc = [
        30,
        3*60+30,
        9*60+30,
        12*60+30,
        15*60+30,
        17*60+30,
        18*60+30,
        24*60+30
    ]
    now = datetime.utcnow()
    target = None
    today = datetime.utcnow().date()
    today = datetime(today.year, today.month, today.day)
    for i, interval in enumerate(boss_times_interval_from_utc):
        next_time_candidate = today + timedelta(minutes=interval)
        if now < next_time_candidate:
            target = i
            break
    next_time = today + timedelta(minutes=boss_times_interval_from_utc[target])
    return next_time


def sinoalice_raid_boss(_msg_info, _robot_settingg):
    # list of time
    next_time = _find_next_boss_time()
    next_time_utc_8 = next_time + timedelta(hours=8)

    ts = int(time.time()) + 3600 * 8
    utc_8_time = datetime.utcfromtimestamp(ts)
    utc_8_time_str = utc_8_time.strftime('%m月%d號 %H點%M分')
    utc_8_next_time_str = next_time_utc_8.strftime('%m月%d號 %H點%M分')
    diff_time_tuple = str(next_time_utc_8 - utc_8_time).split(':')
    diff_hour_str = f'{diff_time_tuple[0]}小時' if int(diff_time_tuple[0]) != 0 else ''
    return f'討伐時間 0830、1130、1730、2030、2330、0130、0230\n' \
        f'現在台灣為 {utc_8_time_str}\n' \
        f'下一個討伐時間為 {utc_8_next_time_str} （{diff_hour_str}{diff_time_tuple[1]}分後）'


def why(_msg_info, _robot_settings):
    random.seed(os.urandom(5))
    return f'因為{random.choice(wtf_reasons.reasons)}。'


def tzguguaning(_msg_info, _robot_settings):
    return '恭迎慈孤觀音⎝༼ ◕д ◕ ༽⎠\n渡世靈顯四方⎝༼ ◕д ◕ ༽⎠'


def gurulingpo(_msg_info, _robot_settings):
    s = '''
*``･*+。
 ｜   `*｡
 ｜     *｡
 ｡∩∧ ∧   *
+   (･∀･ )*｡+ﾟ咕嚕靈波
`*｡ ヽ  つ*ﾟ*
 `･+｡*･`ﾟ⊃ +ﾟ
 ☆  ∪~ ｡*ﾟ
 `･+｡*･+ ﾟ
    '''
    return s
