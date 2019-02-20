import datetime
import logging
import os
import time
import uuid
import yaml

from flask import Flask, request, abort, render_template
from linebot import (
    LineBotApi
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, JoinEvent, LeaveEvent, TextMessage, ImageMessage, TextSendMessage, ImageSendMessage
)

from app.common_reply import common_reply
from app.linebot_model_event_extension import MemberJoinEvent, MemberLeaveEvent
from app.linebot_webhook_extension import WebhookHandlerExtended
from constants import GROUP_MAPPING

logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)
application = Flask(__name__, template_folder='templates')


with open("line_auth_key.yml", 'r') as stream:
    data = yaml.load(stream)
    CHANNEL_ACCESS_TOKEN = data['CHANNEL_ACCESS_TOKEN']
    CHANNEL_SECRET = data['CHANNEL_SECRET']
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandlerExtended(CHANNEL_SECRET)


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
        # logging.info('body: %s', body)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.default()
def default(event):
    if event.source.type == 'room':
        source_id = event.source.room_id
    elif event.source.type == 'user':
        source_id = event.source.user_id
    elif event.source.type == 'group':
        source_id = event.source.group_id
        if source_id == 'C1e38a92f8c7b4ad377df882b9f3bf336' and event.source.user_id == 'U2b7c3a71683ab247b08b1f7845e20df7':
            if event.message.type == 'sticker':
                pid = event.message.package_id
                sid = event.message.sticker_id
                sticker_mapping = {
                    ('3219988', '35156126'): '躲',
                    ('1353138', '14028005'): '躲',
                    ('1300920', '12169612'): '躲',
                    ('1394695', '15335159'): '躲',
                    ('1394695', '15335150'): '看',
                    ('1394695', '15335129'): '笑',
                    ('1394695', '15335126'): '氣',
                    ('1394695', '15335128'): '哭',
                }
                if (pid, sid) in sticker_mapping:
                    reply = [TextSendMessage(text=f"EBB 不要{sticker_mapping['(pid, sid)']}出來嗨ヽ(∀ﾟ )人( ﾟ∀)ﾉ")]
                    line_bot_api.reply_message(event.reply_token, reply)
    else:
        raise ValueError
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')} {event.source.user_id} ：{event.message}")


@handler.add(JoinEvent)
def handle_join_event(event):
    if event.source.type == 'room':
        source_id = event.source.room_id
    elif event.source.type == 'group':
        source_id = event.source.group_id
    else:
        raise ValueError
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')} JoinEvent")
    replies = [TextSendMessage(text=f'安安/ 感謝邀請我進來～')]
    line_bot_api.reply_message(event.reply_token, replies)


@handler.add(LeaveEvent)
def handle_leave_event(event):
    if event.source.type == 'room':
        source_id = event.source.room_id
    elif event.source.type == 'group':
        source_id = event.source.group_id
    else:
        raise ValueError
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')} LeaveEvent")


@handler.add(MemberJoinEvent)
def handle_member_join_event(event):
    if event.source.type == 'room':
        source_id = event.source.room_id
    elif event.source.type == 'group':
        source_id = event.source.group_id
    else:
        raise ValueError
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')}")

    # 可怕的象奶儀式
    if source_id in [
        'C770afed112311f3f980291e1e488e0ef',
        'Cf794cf7dc1970c3fba9122673cf3dcde',
        'C498a6c669b4648d8dcb807415554fda1'
    ]:
        imgur_url = 'https://i.imgur.com/'
        replies_img = ['cLD5pX1.jpg', '0dpXilD.jpg', 'kuHrYI6.jpg']
        replies = [ImageSendMessage(original_content_url=imgur_url + r, preview_image_url=imgur_url + r, ) for r in
                   replies_img]
        # user_ids = [m.user_id for m in event.joined.members]
        # user_names = [line_bot_api.get_profile(uid).display_name for uid in user_ids]
        # replies.append(TextSendMessage(text=f'@{",".join(user_names)} 新人還有呼吸嗎 記得到記事本簽到(上面圖片那篇)'))
        replies.append(TextSendMessage(text=f'新人還有呼吸嗎 記得到記事本簽到(上面圖片那篇)'))
    elif source_id == 'C1e38a92f8c7b4ad377df882b9f3bf336':
        replies = [TextSendMessage(text=f'安安～這裡是清新優質群組，每天有很多車班可以上車學習，願大家都能很快考到駕照～')]
    else:
        return
    line_bot_api.reply_message(event.reply_token, replies)


@handler.add(MemberLeaveEvent)
def handle_member_leave_event(event):
    if event.source.type == 'room':
        source_id = event.source.room_id
    elif event.source.type == 'group':
        source_id = event.source.group_id
    else:
        raise ValueError
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')} 有人退群囉")
    # user_ids = [m.user_id for m in event.joined.members]
    # user_names = [line_bot_api.get_profile(uid).display_name for uid in user_ids]
    # replies = [TextSendMessage(text=f'群友{",".join(user_names)}失去了夢想。')]


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    if event.source.type == 'room':
        source_id = event.source.room_id
    elif event.source.type == 'group':
        source_id = event.source.group_id
    elif event.source.type == 'user':
        source_id = event.source.user_id
    else:
        raise ValueError
    uid = event.source.user_id
    image_id = event.message.id
    message_content = line_bot_api.get_message_content(image_id)
    now = int(time.time())
    date = datetime.datetime.utcfromtimestamp(now)
    date_str = date.strftime('%Y%m%d')
    time_str = date.strftime('%H%M%S')
    filename = uuid.uuid4().hex[:3]
    dir_path = os.path.join('/var', 'line_image', date_str, source_id, uid)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, date_str + time_str + '_' + filename + '.jpg')
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')} saved image: {file_path}")


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # logging.info('%s', event.__dict__)
    if event.source.type == 'room':  # 自訂聊天
        source_id = event.source.room_id
    elif event.source.type == 'user':
        source_id = event.source.user_id
        # profile = line_bot_api.get_profile(source_id)
        # status = f'{profile.display_name} 的顯圖：{profile.picture_url}, 狀態：{profile.status_message}'
    elif event.source.type == 'group':  # 群組
        source_id = event.source.group_id
    else:
        raise ValueError(f" unknown event.source.type: {event.source.type}")
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')} {event.source.user_id} ：{event.message.text}")
    make_reply(event.source.type, source_id, event.message.text, reply_token=event.reply_token)


def make_reply(_source_type, source_id, msg, reply_token=None):
    # private reply
    reply = common_reply(source_id, msg)
    if reply:
        line_bot_api.reply_message(reply_token, reply)
        return

    # group reply
    if source_id not in GROUP_MAPPING:
        return

    reply = GROUP_MAPPING[source_id]['function'](msg)
    if reply:
        line_bot_api.reply_message(reply_token, reply)
        return