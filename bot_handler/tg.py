import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext

from app import dice
from app.ext_apis.tw_open_data import epa_aqi_api, uv_api
from app.ext_apis.util import cartesian
from app.ext_apis.util import reverse_geocode_customize
from app.sqlite_utils.user_location import query_tg_user_location


def bot_help(update: Update, _context: CallbackContext):
    # _args = context.args
    update.message.reply_text('Help!')


def get_location_keyboard_markup():
    location_keyboard = KeyboardButton(text="我要提供位置資訊", request_location=True)
    reject_keyboard = KeyboardButton(text="先不要")
    custom_keyboard = [[location_keyboard, reject_keyboard]]
    markup = ReplyKeyboardMarkup(
        custom_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup


# from Code snippets
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#requesting-location-and-contact-from-user
def set_location(update: Update, _context: CallbackContext):
    update.message.reply_text(
        text="你想提供位置資訊讓朽咪提供更多服務嗎？",
        reply_markup=get_location_keyboard_markup()
    )


def get_weather_data_from_closest_site(lat, lon, json_data, site_tree):
    cartesian_coord = cartesian(lat, lon)
    closest_site = site_tree.query([cartesian_coord], p=2)
    site_index = closest_site[1][0]
    return json_data[site_index]


def weather(update: Update, _context: CallbackContext):
    # _args = context.args
    gps_location = query_tg_user_location(update.effective_user.id)
    lat, lon = gps_location
    if not gps_location:
        update.message.reply_text(
            text='朽咪不知道您的位置資訊，你想提供位置資訊讓朽咪提供更多服務嗎？',
            reply_markup=get_location_keyboard_markup()
        )
    else:
        aqi_json_data, aqi_site_tree = epa_aqi_api()
        aqi_info = get_weather_data_from_closest_site(lat, lon, aqi_json_data, aqi_site_tree)
        aqi_site_name = aqi_info['SiteName']
        aqi_site_county = aqi_info['County']
        aqi = aqi_info['AQI']
        aqi_status = aqi_info['Status']
        pm25 = aqi_info['PM2.5']
        aqi_publish_time = aqi_info['PublishTime']
        uv_json_data, uv_site_tree = uv_api()
        uv_info = get_weather_data_from_closest_site(lat, lon, uv_json_data, uv_site_tree)
        uv_site_name = uv_info['SiteName']
        uv_site_county = uv_info['County']
        uvi = uv_info['UVI']
        uv_publish_time = uv_info['PublishTime']
        geo_info = reverse_geocode_customize((lat, lon))[0]
        update.message.reply_text(
            f'你所在的位置：{geo_info["name"]} (行政區: {geo_info["admin1"]}, 國家: {geo_info["cc"]})\n'
            f'離你最近的測站資訊：\n'
            f'\n'
            f'空品資訊從{aqi_site_name}測站 ({aqi_site_county})\n'
            f'{aqi_status} (AQI: {aqi}, PM2.5: {pm25}) 時間: {aqi_publish_time}\n'
            f'\n'
            f'紫外線資訊從{uv_site_name}測站 ({uv_site_county})\n'
            f'UVI: {uvi} 時間: {uv_publish_time}\n'
        )


def tarot(update: Update, _context: CallbackContext):
    # _args = context.args
    card = dice.draw_tarot()
    update.message.reply_photo(
        photo=card['url'],
        caption=card['nameCN'],
        disable_notification=True,
        reply_to_message_id=update.message.message_id,
    )


def fortune(update: Update, _context: CallbackContext):
    # _args = context.args
    reply = dice.fortune(None, None)
    update.message.reply_text(reply)


def make_reply(update: Update, _context: CallbackContext):
    # _args = context.args
    text = update.message.text
    logger = logging.getLogger(__name__)
    if 'ㄆㄆ' in text:
        reply = '我知道！戳！'
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


def add_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("help", bot_help, pass_args=True))
    dispatcher.add_handler(CommandHandler("setlocation", set_location, pass_args=True))
    dispatcher.add_handler(CommandHandler("weather", weather, pass_args=True))
    dispatcher.add_handler(CommandHandler("tarot", tarot, pass_args=True))
    dispatcher.add_handler(CommandHandler("fortune", fortune, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.text, make_reply))
