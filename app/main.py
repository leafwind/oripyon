import logging

from flask import Flask, request, abort, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)


from line_auth_key import CHANNEL_SECRET, CHANNEL_ACCESS_TOKEN
from app.common_reply import common_reply
from app.group_reply import group_reply_test, group_reply_lineage_m, group_reply_maplestory, group_reply_yebai
from app.group_reply import group_reply_mao_sino_alice, group_reply_nier_sino_alice, group_reply_luna
from app.group_reply import group_reply_working, group_reply_taiwan_sino_alice

logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)
application = Flask(__name__, template_folder='templates')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

GROUP_MAPPING = {
    'C1bebaeaf89242089f0d755d492df6cb6': {
        'name': '測試群組',
        'function': group_reply_test,
    },
    'C690e08d2fb900d5bbd873e103d500b92': {
        'name': '皇家御貓園',
        'function': group_reply_luna,
    },
    'C25add4301bc790a641e07b02b868a9b7': {
        'name': '葉白',
        'function': group_reply_yebai,
    },
    'C0cd56d37156c5ad3fe04b702624d50dd': {
        'name': '小路北七群',
        'function': group_reply_maplestory,
    },
    'C966396824051cbb00e35af7b4123a0a5': {
        'name': '天堂老司機',
        'function': group_reply_lineage_m,
    },
    'Cfb6a76351d112834244144a1cd4f0f57': {
        'name': '死愛魔王城',
        'function': group_reply_mao_sino_alice,
    },
    'C1e38a92f8c7b4ad377df882b9f3bf336': {
        'name': '尼爾主題餐廳',
        'function': group_reply_nier_sino_alice,
    },
    'C15c762c0a497d62992c01b42ba9b39d9': {
        'name': '死愛台版交流區',
        'function': group_reply_taiwan_sino_alice,
    },
    'Cbc420349e56f3bae5d5f46fafb0ac5cb': {
        'name': '社畜人生的煩惱',
        'function': group_reply_working,
    }
}


@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@application.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    application.logger.info("Request body: " + body)

    # handle Web hook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.default()
def default(event):
    logging.info('{}'.format(event.message))
    if event.source.type == 'room':
        source_id = event.source.room_id
    elif event.source.type == 'user':
        source_id = event.source.user_id
    elif event.source.type == 'group':
        source_id = event.source.group_id
        if source_id == 'C1e38a92f8c7b4ad377df882b9f3bf336':
            if event.message.type == 'sticker':
                if event.message.package_id == '1394695':
                    if event.message.sticker_id == '15335159':
                        reply = [TextSendMessage(text='EBB 不要躲出來嗨 ヽ(∀ﾟ )人( ﾟ∀)ﾉ')]
                        line_bot_api.reply_message(event.reply_token, reply)
    else:
        raise ValueError
    logging.info('{}：{}'.format(GROUP_MAPPING.get(source_id, {'name': source_id}).get('name'), event.message))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # logging.info('%s', event.__dict__)
    if event.source.type == 'room':  # 自訂聊天
        source_id = event.source.room_id
    elif event.source.type == 'user':
        source_id = event.source.user_id
        # profile = line_bot_api.get_profile(source_id)
        # status = '{} 的顯圖：{}, 狀態：{}'.decode('utf-8').format(profile.display_name, profile.picture_url,
        #                                                    profile.status_message)
    elif event.source.type == 'group':  # 群組
        source_id = event.source.group_id
    else:
        raise ValueError
    make_reply(event.source.type, source_id, event.message.text, reply_token=event.reply_token)


def make_reply(_source_type, source_id, msg, reply_token=None):
    logging.info('{}：{}'.format(GROUP_MAPPING.get(source_id, {'name': source_id}).get('name'), msg))
    reply = common_reply(source_id, msg)
    if reply:  # has reply, no need to search group reply
        line_bot_api.reply_message(reply_token, reply)
        return

    if source_id not in GROUP_MAPPING:
        return

    reply = GROUP_MAPPING[source_id]['function'](msg)
    if reply:
        line_bot_api.reply_message(reply_token, reply)
        return
