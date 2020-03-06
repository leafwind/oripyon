import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext
from telegram.files.inputmedia import InputMediaPhoto

from app import dice
from app.ext_apis.dxy_open_data import load_ncov_data
from app.ext_apis.tw_open_data import epa_aqi_api, uv_api
from app.ext_apis.util import cartesian
from app.ext_apis.util import reverse_geocode_customize
from app.sqlite_utils.user_location import check_or_create_table_tg_user_location, insert_tg_user_location
from app.sqlite_utils.user_location import query_tg_user_location


def get_function_keyboard_markup(chat_type):
    weather_button = KeyboardButton(text='\U00002603 天氣')
    tarot_button = KeyboardButton(text='\U0001F0CF 塔羅')
    fortune_button = KeyboardButton(text='\U0001F3B0 運勢')
    ncov_button = KeyboardButton(text='\U0001F637　武漢肺炎')
    touch_schumi_button = KeyboardButton(text='\U0001F430 摸朽咪')
    feedback_button = KeyboardButton(text='\U0001F4E8 建議交流')
    # “private”, “group”, “supergroup” or “channel”
    if chat_type != 'private':
        set_location_button = KeyboardButton(text='\U0001F4CD 設定位置')
    else:
        set_location_button = KeyboardButton(text='\U0001F4CD 設定位置', request_location=True)
    close_button = KeyboardButton(text='\U0000274E 關閉鍵盤')
    custom_keyboard = [
        [weather_button, tarot_button, fortune_button],
        [ncov_button, touch_schumi_button, feedback_button],
        [set_location_button, close_button]
    ]
    markup = ReplyKeyboardMarkup(
        custom_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup


def bot_help(update: Update, _context: CallbackContext):
    # _args = context.args
    update.message.reply_text(
        text=f'你可以：\n'
             f'輸入 "/" 展開指令選單\n'
             f'使用貼圖旁邊的 [ / ] 按鈕展開指令選單\n'
             f'使用下面的鍵盤選單',
        reply_markup=get_function_keyboard_markup(update.message.chat.type)
    )


def get_ncov_keyboard_markup():
    korea_button = KeyboardButton(text='\U0001F1F0\U0001F1F7 韓國')
    japan_button = KeyboardButton(text='\U0001F1EF\U0001F1F5 日本')
    italy_button = KeyboardButton(text='\U0001F1EE\U0001F1F9 義大利')
    iran_button = KeyboardButton(text='\U0001F1EE\U0001F1F7 伊朗')
    reject_button = KeyboardButton(text='\U0000274E 關閉鍵盤')
    custom_keyboard = [
        [korea_button, japan_button, italy_button, iran_button],
        [reject_button]
    ]
    markup = ReplyKeyboardMarkup(
        custom_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup


def get_location_keyboard_markup():
    location_button = KeyboardButton(text='我要提供位置資訊', request_location=True)
    reject_button = KeyboardButton(text='\U0000274E 關閉鍵盤')
    custom_keyboard = [[location_button, reject_button]]
    markup = ReplyKeyboardMarkup(
        custom_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup


def get_weather_data_from_closest_site(lat, lon, json_data, site_tree):
    """
    use K-D tree to find closet place
    ref: https://www.timvink.nl/closest-coordinates/
    :param lat:
    :param lon:
    :param json_data:
    :param site_tree:
    :return:
    """
    cartesian_coord = cartesian(lat, lon)
    closest_site = site_tree.query([cartesian_coord], p=2)
    site_index = closest_site[1][0]
    return json_data[site_index]


def weather(update: Update, _context: CallbackContext):
    # _args = context.args
    gps_location = query_tg_user_location(update.effective_user.id)
    if not gps_location:
        if update.message.chat.type == 'private':
            reply = '朽咪不知道您的位置資訊，你想提供位置資訊讓朽咪提供更多服務嗎？'
            logging.getLogger(__name__).info(f'reply: {reply}')
            update.message.reply_text(
                text=reply,
                reply_markup=get_location_keyboard_markup()
            )
        else:
            reply = '朽咪不知道您的位置資訊，請點擊 @oripyon_bot 打開對話以提供位置'
            logging.getLogger(__name__).info(f'reply: {reply}')
            update.message.reply_text(
                text=reply
            )
    else:
        lat, lon = gps_location
        update.message.reply_text(text='自動取用離你最近的測站天氣資料中，目前僅限台灣國內才能正常使用', disable_notification=True)
        update.message.reply_text(text='取得環保署即時空品資料中...', disable_notification=True)
        aqi_json_data, aqi_site_tree = epa_aqi_api()
        aqi_info = get_weather_data_from_closest_site(lat, lon, aqi_json_data, aqi_site_tree)
        aqi_site_name = aqi_info['SiteName']
        aqi_site_county = aqi_info['County']
        aqi = aqi_info['AQI']
        aqi_status = aqi_info['Status']
        pm25 = aqi_info['PM2.5']
        aqi_publish_time = aqi_info['PublishTime']
        update.message.reply_text(text='取得環保署即時紫外線資料中...', disable_notification=True)
        uv_json_data, uv_site_tree = uv_api()
        uv_info = get_weather_data_from_closest_site(lat, lon, uv_json_data, uv_site_tree)
        uv_site_name = uv_info['SiteName']
        uv_site_county = uv_info['County']
        uvi = uv_info['UVI']
        uv_publish_time = uv_info['PublishTime']
        geo_info = reverse_geocode_customize((lat, lon))[0]
        update.message.reply_text(
            f'\U0001F310 你所在的位置：{geo_info["name"]} (行政區: {geo_info["admin1"]}, 國家: {geo_info["cc"]})\n'
            f'離你最近的測站資訊：\n'
            f'\n'
            f'\U0001F4A8 空品資訊從{aqi_site_name}測站 ({aqi_site_county})\n'
            f'\U000027A1 {aqi_status} (AQI: {aqi}, PM2.5: {pm25})\n'
            f'\U0000231A 時間: {aqi_publish_time}\n'
            f'\n'
            f'\U0001F506 紫外線資訊從{uv_site_name}測站 ({uv_site_county})\n'
            f'\U000027A1 UVI: {uvi} \n'
            f'\U0000231A 時間: {uv_publish_time}\n'
        )


def tarot(update: Update, _context: CallbackContext):
    # _args = context.args
    card = dice.draw_tarot()
    logging.getLogger(__name__).info(f'reply: {card}')
    update.message.reply_photo(
        photo=card['url'],
        caption=card['nameCN'],
        disable_notification=True,
        reply_to_message_id=update.message.message_id,
    )


def fortune(update: Update, _context: CallbackContext):
    # _args = context.args
    reply = dice.fortune(None, None)
    logging.getLogger(__name__).info(f'reply: {reply}')
    update.message.reply_text(reply)


def dummy_reply(update: Update, _context: CallbackContext):
    reply = '什麼事都沒發生，就跟你說別按齁 \U0001F430'
    logging.getLogger(__name__).info(f'reply: {reply}')
    update.message.reply_text(reply)


def ncov_reply(update: Update, _context: CallbackContext):
    reply = '請選擇要查詢的災區國家 \U0001F430'
    update.message.reply_text(
        text=reply,
        reply_markup=get_ncov_keyboard_markup()
    )


def query_ncov(update: Update, _context: CallbackContext, country):
    country_image_url = load_ncov_data()
    media_group = []
    for key in country_image_url:
        if key.startswith(country):
            media_group.append(InputMediaPhoto(media=country_image_url[key], caption=key))
    update.message.reply_media_group(
        media=media_group,
        disable_notification=True,
    )


def touch_schumi(update: Update, _context: CallbackContext):
    reply = dice.touch_schumi()
    logging.getLogger(__name__).info(f'reply: {reply}')
    update.message.reply_text(reply)


def feedback(update: Update, _context: CallbackContext):
    reply = f'聯絡作者 @leafwind_tw\n' \
            f'朽咪公開聊天區 @oripyon_talk'
    update.message.reply_text(reply)


# from Code snippets
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#requesting-location-and-contact-from-user
def set_location(update: Update, _context: CallbackContext):
    if update.message.chat.type == 'private':
        reply = '你想提供位置資訊讓朽咪提供更多服務嗎？'
        logging.getLogger(__name__).info(f'reply: {reply}')
        update.message.reply_text(
            text=reply,
            reply_markup=get_location_keyboard_markup()
        )
    else:
        reply = '抱歉，位置只支援私訊朽咪 @oripyon_bot 提供'
        logging.getLogger(__name__).info(f'reply: {reply}')
        update.message.reply_text(
            text=reply
        )


def close_keyboard(update: Update, _context: CallbackContext):
    reply = 'OK!\U0001F430'
    logging.getLogger(__name__).info(f'reply: {reply}')
    update.message.reply_text(reply, reply_markup=ReplyKeyboardRemove())


def make_reply(update: Update, _context: CallbackContext):
    # _args = context.args
    if not update.message.text:
        logging.warning(f'no text attribute in: {update.message}')
    text = update.message.text
    logger = logging.getLogger(__name__)
    if text == '\U00002603 天氣':
        weather(update, _context)
    elif text == '\U0001F0CF 塔羅':
        tarot(update, _context)
    elif text == '\U0001F3B0 運勢':
        fortune(update, _context)
    elif text == '\U0001F637　武漢肺炎':
        ncov_reply(update, _context)
    elif text == '\U0001F430 摸朽咪':
        touch_schumi(update, _context)
    elif text == '\U0001F4E8 建議交流':
        feedback(update, _context)
    elif text == '\U0001F4CD 設定位置':
        set_location(update, _context)
    elif text == '\U0000274E 關閉鍵盤':
        close_keyboard(update, _context)
    elif text == '\U0001F1F0\U0001F1F7 韓國':
        query_ncov(update, _context, 'korea')
    elif text == '\U0001F1EF\U0001F1F5 日本':
        query_ncov(update, _context, 'japan')
    elif text == '\U0001F1EE\U0001F1F9 義大利':
        query_ncov(update, _context, 'italy')
    elif text == '\U0001F1EE\U0001F1F7 伊朗':
        query_ncov(update, _context, 'iran')
    elif 'ㄆㄆ' in text:
        reply = '我知道！戳！\U0001F430'
        logger.info(f'reply: {reply}')
        update.message.reply_text(reply)
    elif '我看了' in text:
        update.message.reply_sticker(
            sticker='CAACAgUAAxkBAAMrXlNbUucnbiBebclIoM_qSMb52-sAAjoBAALvY54jySoLvI3DgmEYBA',
            disable_notification=True,
            reply_to_message_id=update.message.message_id,
        )
    elif '沒事了' in text:
        reply = '沒事就好\U0001F430'
        logger.info(f'reply: {reply}')
        update.message.reply_text(reply)


def receive_location(update: Update, _context: CallbackContext):
    location = update.message.location
    lat = location.latitude
    lon = location.longitude
    user = update.effective_user
    update.message.reply_text(
        f'您的資訊將會被朽咪記住，天氣預測功能將根據以下這些資訊提供服務：\n'
        f'\U0001F194 {user.id}\n'
        f'\U00003294 first name: {user.first_name}\n'
        f'\U0001F464 username: {user.username}\n'
        f'\U0001F310 經緯度: {lat}, {lon}'
    )
    check_or_create_table_tg_user_location()
    insert_tg_user_location(user.id, user.first_name, user.username, lat, lon)


def receive_sticker(update: Update, _context: CallbackContext):
    logger = logging.getLogger(__name__)
    logger.info(f'sticker file_id: {update.message.sticker.file_id}')


def add_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("help", bot_help, pass_args=True))
    dispatcher.add_handler(CommandHandler("weather", weather, pass_args=True))
    # dispatcher.add_handler(CommandHandler("tarot", tarot, pass_args=True))
    # dispatcher.add_handler(CommandHandler("fortune", fortune, pass_args=True))
    dispatcher.add_handler(CommandHandler("setlocation", set_location, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.text, make_reply))
    dispatcher.add_handler(MessageHandler(Filters.location, receive_location))
    dispatcher.add_handler(MessageHandler(Filters.sticker, receive_sticker))
