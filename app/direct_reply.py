import random
import os
from app import wtf_reasons
from app.emoji_list import cry_emoji_list


def bot_help():
    return '說明網頁 https://oripyon.weebly.com\n原始碼 https://github.com/leafwind/line_bot'


def poor_chinese():
    return '我覺的台灣人的中文水準以經爛ㄉ很嚴重 大家重來都不重視 因該要在加強 才能越來越利害'


def qq():
    return f'幫QQ喔 {random.choice(cry_emoji_list)}'


def mahoshoujo():
    return '／人◕ ‿‿ ◕人＼ 僕と契約して、魔法少女になってよ！'


def why():
    random.seed(os.urandom(5))
    return f'因為{random.choice(wtf_reasons.reasons)}。'


def gurulingpo():
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