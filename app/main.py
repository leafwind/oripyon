import datetime
import json
import logging
import os
import time
import uuid

import cachetools.func
import gspread
import yaml
from flask import Flask, request, abort, render_template
from linebot import WebhookHandler
from linebot.api import LineBotApi
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, JoinEvent, LeaveEvent, FollowEvent, MemberJoinedEvent, MemberLeftEvent,
    TextMessage, ImageMessage, AudioMessage, TextSendMessage, ImageSendMessage, StickerMessage
)

from announcement_log import check_or_create_table_line_announcement_log, \
    insert_line_announcement_log, query_line_announcement_log
from app.common_reply import common_reply
from app.group_reply import GROUP_MAPPING
from app.private_reply import private_reply
from app.utils.gspread_util import auth_gss_client
from constants import GOOGLE_AUTH_JSON_PATH, GSPREAD_KEY_VIP

logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("oauth2client.crypt").setLevel(logging.WARNING)
application = Flask(__name__, template_folder='templates')

user_info = {}
USER_INFO_MAP_FILE = os.path.join('line-user-info', 'users.json')
if os.path.exists(USER_INFO_MAP_FILE):
    with open(USER_INFO_MAP_FILE, 'r') as _f:
        user_info = json.load(_f)

with open("line_auth_key.yml", 'r') as stream:
    data = yaml.load(stream)
    CHANNEL_ACCESS_TOKEN = data['CHANNEL_ACCESS_TOKEN']
    CHANNEL_SECRET = data['CHANNEL_SECRET']
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


def write_temp_user_mapping(uid, user_name):
    temp_map_file = os.path.join('line-user-info', 'users_temp.txt')
    with open(temp_map_file, 'a') as f:
        f.write(f'\"{uid}\": \"{user_name}\",\n')


@cachetools.func.ttl_cache(ttl=86400)
def get_vip_groups_users():
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    gss_client = auth_gss_client(GOOGLE_AUTH_JSON_PATH, gss_scopes)
    sh = gss_client.open_by_key(GSPREAD_KEY_VIP)
    vip_groups = vip_users = None
    try:
        worksheet = sh.worksheet('vip group')
        vip_groups = worksheet.get_all_values()
        vip_groups = [g[0] for g in vip_groups]
    except gspread.exceptions.WorksheetNotFound as e:
        logging.exception(e)
    try:
        worksheet = sh.worksheet('vip user')
        vip_users = worksheet.get_all_values()
        vip_users = [u[0] for u in vip_users]
    except gspread.exceptions.WorksheetNotFound as e:
        logging.exception(e)
    return vip_groups, vip_users


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
    else:
        raise ValueError
    uid = event.source.user_id
    user_name = user_info.get(uid, None)
    if not user_name:
        try:
            user_name = line_bot_api.get_group_member_profile(source_id, uid).display_name
            write_temp_user_mapping(uid, user_name)
        except LineBotApiError as e:
            logging.debug('LineBotApiError: %s', e)
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')} {user_name}：(default handler){event.message}")


@handler.add(FollowEvent)
def handle_follow_event(event):
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
    replies = [
        TextSendMessage(text=f'安安/ 感謝邀請我進來～／人◕ ‿‿ ◕人＼'),
        TextSendMessage(text=f'為了確保您了解隱私方面的疑慮，請先閱讀使用須知，另外使用手冊也在同一處 https://oripyon.weebly.com'),
        TextSendMessage(text=f'請務必也加飼育員為好友 https://line.me/R/ti/p/%40026hfcxi ，這樣功能更動或維修時才能通知你喔！'),
        TextSendMessage(text=f'如果有些功能無法使用，可能是因為你沒有申請的關係，也請私訊飼育員詢問。'),
    ]
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


@handler.add(MemberJoinedEvent)
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
        'Cfbbdac072c508472fd3acc9ac8fa7adc',
        'Cf794cf7dc1970c3fba9122673cf3dcde',
        'C498a6c669b4648d8dcb807415554fda1'
    ]:
        imgur_url = 'https://i.imgur.com/'
        replies_img = ['cLD5pX1.jpg', '0dpXilD.jpg', 'srpzgjG.jpg']
        replies = [ImageSendMessage(original_content_url=imgur_url + r, preview_image_url=imgur_url + r, ) for r in
                   replies_img]
        replies.append(TextSendMessage(text=f'新人還有呼吸嗎 記得到記事本簽到(上面圖片那篇)'))
    else:
        return
    line_bot_api.reply_message(event.reply_token, replies)


@handler.add(MemberLeftEvent)
def handle_member_leave_event(event):
    if event.source.type == 'room':
        source_id = event.source.room_id
    elif event.source.type == 'group':
        source_id = event.source.group_id
    else:
        raise ValueError
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')} 有人退群囉")


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    if event.source.type == 'room':
        source_id = event.source.room_id
    elif event.source.type == 'group':
        source_id = event.source.group_id
    elif event.source.type == 'user':
        source_id = event.source.user_id
    else:
        raise ValueError
    pid = event.message.package_id
    sid = event.message.sticker_id
    uid = event.source.user_id
    user_name = user_info.get(uid, None)
    if not user_name:
        try:
            user_name = line_bot_api.get_group_member_profile(source_id, uid).display_name
            write_temp_user_mapping(uid, user_name)
        except LineBotApiError as e:
            logging.debug('LineBotApiError: %s', e)
    # sticker_url = f'https://stickershop.line-scdn.net/stickershop/v1/sticker/{sid}/android/sticker.png'
    # logging.info(
    #     f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')}"
    #     f"{user_name}({uid}) (sticker) ({pid}, {sid}), url: {sticker_url}"
    # )


@handler.add(MessageEvent, message=[ImageMessage,AudioMessage])
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
    message_content = line_bot_api.get_message_content(event.message.id)
    now = int(time.time())
    date = datetime.datetime.utcfromtimestamp(now)
    date_str = date.strftime('%Y%m%d')
    time_str = date.strftime('%H%M%S')
    filename = uuid.uuid4().hex[:3]
    dir_path = os.path.join('/var', 'line_image', date_str, source_id, uid)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    if event.message.type == 'image':
        extension = 'jpg'
    elif event.message.type == 'audio':
        extension = 'aac'
    else:
        raise TypeError
    file_path = os.path.join(dir_path, date_str + time_str + '_' + filename + '.' + extension)
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    uid = event.source.user_id
    user_name = user_info.get(uid, None)
    if not user_name:
        try:
            user_name = line_bot_api.get_group_member_profile(source_id, uid).display_name
            write_temp_user_mapping(uid, user_name)
        except LineBotApiError as e:
            logging.debug('LineBotApiError: %s', e)
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')} {user_name} (image) saved: {file_path}")


class MessageInfo:
    def __init__(self, source_type, source_id, uid, user_name, msg):
        self.source_type = source_type
        self.source_id = source_id
        self.user_name = user_name
        self.uid = uid
        self.msg = msg


class RobotSettings:
    def __init__(self, vip_groups, vip_users):
        self.vip_groups = vip_groups
        self.vip_users = vip_users


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
    uid = event.source.user_id
    user_name = user_info.get(uid, None)
    if not user_name:
        try:
            user_name = line_bot_api.get_group_member_profile(source_id, uid).display_name
            write_temp_user_mapping(uid, user_name)
        except LineBotApiError:
            pass  # try room member profile
        try:
            user_name = line_bot_api.get_room_member_profile(source_id, uid).display_name
            write_temp_user_mapping(uid, user_name)
        except LineBotApiError as e:
            logging.debug('LineBotApiError: %s, source_id: %s, uid: %s', e, source_id, uid)
    logging.info(
        f"{GROUP_MAPPING.get(source_id, {'name': source_id}).get('name')} {user_name}：{event.message.text}")

    vip_groups, vip_users = get_vip_groups_users()
    msg_info = MessageInfo(event.source.type, source_id, uid, user_name, event.message.text)
    robot_settings = RobotSettings(vip_groups, vip_users)
    make_reply(msg_info, robot_settings, reply_token=event.reply_token)

    if source_id in GROUP_MAPPING and 'log_filename' in GROUP_MAPPING[source_id]:
        log_filename = GROUP_MAPPING[source_id]['log_filename'] + '.txt'
    else:
        log_filename = source_id + '.txt'

    dir_path = os.path.join('/var', 'line_log')
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    with open(os.path.join(dir_path, log_filename), 'a') as fp:
        now = int(time.time())
        date = datetime.datetime.utcfromtimestamp(now)
        date = date + datetime.timedelta(hours=8)
        time_str = date.strftime('%Y%m%d:%H%M%S')
        fp.write(f"{time_str} {user_name}：{event.message.text}\n")
    # chat(line_bot_api, event.reply_token, source_id, event.msg.text, log_filename)


def get_announcement(source_id):
    # common reply 塞公告
    check_or_create_table_line_announcement_log()
    max_ts = query_line_announcement_log(source_id)
    now_ts = int(time.time())
    announcement_file = os.path.join('./announcement.json')
    if now_ts//86400 == max_ts//86400:
        # same day, skip
        return None
    elif now_ts - max_ts <= 12*3600:
        # not over 12 hrs
        return None
    elif not os.path.exists(announcement_file):
        return None
    else:
        with open(announcement_file, 'r') as f:
            announcement = json.load(f)
        date_begin = datetime.datetime.strptime(announcement[0]['date_begin'], '%Y-%m-%d')
        date_end = datetime.datetime.strptime(announcement[0]['date_end'], '%Y-%m-%d')
        begin_ts = time.mktime(date_begin.timetuple())
        end_ts = time.mktime(date_end.timetuple())
        if begin_ts < now_ts < end_ts:
            announcement_text_list = announcement[0]['content']
            insert_line_announcement_log(source_id, now_ts)
            return announcement_text_list
        else:
            return None


def make_reply(msg_info, robot_settings, reply_token=None):
    # private reply, only
    if msg_info.source_type == 'user':
        reply = private_reply(msg_info, robot_settings)
        if reply:
            line_bot_api.reply_message(reply_token, reply)
            return

    # common reply
    reply = common_reply(msg_info, robot_settings)
    announcement_text_list = get_announcement(msg_info.source_id)
    if announcement_text_list:
        for text in announcement_text_list:
            reply.append(TextSendMessage(text=text))
    if reply:
        line_bot_api.reply_message(reply_token, reply)
        return

    # group specific reply
    if msg_info.source_id not in GROUP_MAPPING:
        return

    reply = GROUP_MAPPING[msg_info.source_id]['function'](line_bot_api, msg_info.source_id, msg_info.uid, msg_info.msg)
    if reply:
        line_bot_api.reply_message(reply_token, reply)
        return
