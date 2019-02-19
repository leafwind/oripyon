# Line Bot [![Build Status](https://travis-ci.org/leafwind/line_bot.svg?branch=master)](https://travis-ci.org/leafwind/line_bot) [![Coverage Status](https://coveralls.io/repos/github/leafwind/line_bot/badge.svg?branch=master)](https://coveralls.io/github/leafwind/line_bot?branch=master)

Simple bot build by [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)

## Bot Administration

Go to [LINE@ MANAGER](https://admin-official.line.me/)

- Account Overview -> (Select Your Account) -> Account Setting

Basic Setting:

- Set profile image
- Get QR code / Add friend button

Bot Setting:

- Webhook Messaging Allow/Disallow
- Allow to be add in group chat Y/N
- Auto response Y/N
- Greetings Y/N

## Get Channel Secret and Channel Access Token

Go to [Business Center](https://business.line.me/zh-hant/)

- Account List -> Your Accounts -> Messaging API -> LINE Developers
- Fill `line_auth_key.py` with secret and access token
- `CHANNEL_SECRET = ''`
- `CHANNEL_ACCESS_TOKEN = ''`

# Development

- build environment with python 3.7: `./scripts/build_venv.sh`
- init and update submodule: `git submodule update --init --recursive`

## Restart uwsgi to apply code change

`sudo systemctl restart line_bot_uwsgi`

## Debug

`tail -f /var/log/uwsgi/uwsgi.log -n 100`

## 機器人指令表

【一般天氣指令】

使用中央氣象局最新資料

◉ 天氣 -> 天氣概況圖（以10分鐘為單位更新）

◉ 即時雨量 -> 即時雨量圖（以30分鐘為單位更新）

◉ 雷達 -> 雷達回波圖（以10分鐘為單位更新）

◉ 空品 -> 空氣品質圖（以60分鐘為單位更新）

◉ 空品預測[空格][地區] -> 空氣品質預測（僅能預測粗略空品區）

◉ 空品現況[空格][地區] -> 空氣品質現況（列出該縣市所有測站資訊）

【其他指令】

◉ 包含「幫QQ」 -> 機器人幫邊緣的你QQ

◉ 包含「運勢」-> 抽運勢

◉ 包含「塔羅」-> 抽塔羅牌（厭世動物園畫風）

◉ 包含「咕嚕靈波」

◉ 包含「爛中文」

◉ 包含「魔法少女」
◉ 包含「請問為什麼」

## Ref.

- [link 1](http://qiita.com/Kosuke-Szk/items/e31df8665f2a83406362)
- [link 2](http://qiita.com/mochan_tk/items/db3fd4e4867dd3fb6540)
- [Line Messaging API](https://developers.line.biz/en/reference/messaging-api/#text-message)
- [Emoji Unicode Tables](https://apps.timwhitlock.info/emoji/tables/unicode)
- [Emoji supported by Line bot](https://developers.line.biz/media/messaging-api/emoji-list.pdf)
- [Sticker supported by Line bot](https://developers.line.biz/media/messaging-api/messages/sticker_list.pdf)
- 匯率查詢來自[全球即時匯率API](https://tw.rter.info/howto_currencyapi.php)
