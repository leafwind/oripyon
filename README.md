# Line Bot

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

# Development

- build environment with python 3.7: `./scripts/build_venv.sh`

## Restart uwsgi to apply code change

`sudo systemctl restart line_bot_uwsgi`

## Debug

`tail -f /var/log/uwsgi/uwsgi.log -n 100`

## Ref.

- [link 1](http://qiita.com/Kosuke-Szk/items/e31df8665f2a83406362)
- [link 2](http://qiita.com/mochan_tk/items/db3fd4e4867dd3fb6540)
- [Line Messaging API](https://developers.line.biz/en/reference/messaging-api/#text-message)
- [Emoji Unicode Tables](https://apps.timwhitlock.info/emoji/tables/unicode)
- [Emoji supported by Line bot](https://developers.line.biz/media/messaging-api/emoji-list.pdf)
- [Sticker supported by Line bot](https://developers.line.biz/media/messaging-api/messages/sticker_list.pdf)
- 匯率查詢來自[全球即時匯率API](https://tw.rter.info/howto_currencyapi.php)
