import os
import random

from app import wtf_reasons
from app.emoji_list import CRY_EMOJI_LIST


def pier_girl(msg_info, robot_settings):
    random.seed(os.urandom(5))
    return random.choice(
        [
            'https://www.youtube.com/watch?v=BoD4yCTXTCU',
            'https://www.youtube.com/watch?v=M-MT0z6ac7g'
        ]
    )


def girlfriend(msg_info, robot_settings):
    return [('image', 'https://i.imgur.com/g6WRWrk.jpg')]


def daughter_red(msg_info, robot_settings):
    replies = [('image', 'https://i.imgur.com/vKGB3XM.jpg'), ('text', '杜家庄女兒紅 七日釀造 七星獎 口碑88分')]
    return replies


def bot_help(msg_info, robot_settings):
    return '說明網頁 https://oripyon.weebly.com\n原始碼 https://github.com/leafwind/line_bot'


def poor_chinese(msg_info, robot_settings):
    return '我覺的台灣人的中文水準以經爛ㄉ很嚴重 大家重來都不重視 因該要在加強 才能越來越利害'


def qq(msg_info, robot_settings):
    random.seed(os.urandom(5))
    return f'幫QQ喔 {random.choice(CRY_EMOJI_LIST)}'


def mahoshoujo(msg_info, robot_settings):
    return '／人◕ ‿‿ ◕人＼ 僕と契約して、魔法少女になってよ！'


def why(msg_info, robot_settings):
    random.seed(os.urandom(5))
    return f'因為{random.choice(wtf_reasons.reasons)}。'


def tzguguaning(msg_info, robot_settings):
    return '恭迎慈孤觀音⎝༼ ◕д ◕ ༽⎠\n渡世靈顯四方⎝༼ ◕д ◕ ༽⎠'


def gurulingpo(msg_info, robot_settings):
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