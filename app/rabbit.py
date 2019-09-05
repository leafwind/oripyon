import datetime
import logging
import sqlite3
import time
from contextlib import closing

import cachetools.func
from linebot.models import (
    MessageAction, FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    ButtonComponent, TextComponent, SeparatorComponent
)

from app.utils.sqlite_util import table_exists
from constants import LINE_DB_PATH, TABLE_RABBIT_FEEDING


@cachetools.func.ttl_cache(ttl=86400)
def my_rabbit_exists(uid):
    with closing(sqlite3.connect(LINE_DB_PATH)) as conn, closing(conn.cursor()) as c:
        query = f"SELECT count(1) FROM {TABLE_RABBIT_FEEDING} WHERE uid=:uid;"
        c.execute(query, {'uid': uid})
        (count,) = c.fetchone()
        logging.warning(f'{uid} has {count} rabbit')
        if count > 0:
            return True
        else:
            return False


def adopt_rabbit(msg_info, _robot_settings):
    if my_rabbit_exists(msg_info.uid):
        return [('text', '你已經有一隻兔子啦')]
    else:
        with closing(sqlite3.connect(LINE_DB_PATH)) as conn, closing(conn.cursor()) as c:
            now = int(time.time())
            insert_sql = f'''
                INSERT INTO {TABLE_RABBIT_FEEDING} (uid, born_ts) VALUES (:uid, :born_ts);
            '''
            c.execute(insert_sql, {'uid': msg_info.uid, 'born_ts': now})
            conn.commit()
        time_str = (datetime.datetime.utcfromtimestamp(now) + datetime.timedelta(hours=8))\
            .strftime('%Y-%m-%d %H:%M:%S')
        return [('text', f'已經領養完畢，他的出生時間是 {time_str}')]


def my_rabbit(msg_info, _robot_settings):
    if not table_exists(TABLE_RABBIT_FEEDING):
        check_or_create_table_rabbit_feeding()

    if not my_rabbit_exists(msg_info.uid):
        container = build_rabbit_adopt_content()
        return [('flex', FlexSendMessage(alt_text='請到手機確認是否領養', contents=container))]
    else:
        with closing(sqlite3.connect(LINE_DB_PATH)) as conn, closing(conn.cursor()) as c:
            query = f'''
                SELECT
                born_ts,
                strength,
                agility,
                intelligence,
                affection,
                satiation
                FROM {TABLE_RABBIT_FEEDING} WHERE uid=:uid
            '''
            c.execute(query, {'uid': msg_info.uid})
            (born_ts, strength, agility, intelligence, affection, satiation) = c.fetchone()
            container = build_rabbit_card_content(born_ts, strength, agility, intelligence, affection, satiation)
            return [('flex', FlexSendMessage(alt_text="請到手機查看兔子資訊", contents=container))]


def check_or_create_table_rabbit_feeding():
    with closing(sqlite3.connect(LINE_DB_PATH)) as conn, closing(conn.cursor()) as c:
        create_sql = f'''
            CREATE TABLE IF NOT EXISTS {TABLE_RABBIT_FEEDING}
            (
                uid text,
                born_ts int,
                strength int DEFAULT 0,
                agility int DEFAULT 0,
                intelligence int DEFAULT 0,
                affection int DEFAULT 0,
                satiation int DEFAULT 0,
                PRIMARY KEY (uid)
            )
        '''
        c.execute(create_sql)
        conn.commit()


def insert_rabbit_feeding(uid):
    with closing(sqlite3.connect(LINE_DB_PATH)) as conn, closing(conn.cursor()) as c:
        insert_sql = f'''
            INSERT OR REPLACE INTO {TABLE_RABBIT_FEEDING} VALUES (:uid, :born_ts);
        '''
        c.execute(insert_sql, {'uid': uid, 'born_ts': int(time.time())})
        conn.commit()


def build_rabbit_adopt_content():
    container = BubbleContainer(
        direction='ltr',
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(text='你還沒有兔子', weight='bold', size='xl'),
                SeparatorComponent(),
                BoxComponent(
                    layout='horizontal',
                    spacing='sm',
                    contents=[
                        ButtonComponent(
                            style='primary',
                            height='sm',
                            color='#95B9B4',
                            action=MessageAction(label='領養兔子', text='領養兔子'),
                        ),
                        ButtonComponent(
                            style='primary',
                            height='sm',
                            color='#95B9B4',
                            action=MessageAction(label='沒事了', text='沒事了')
                        )
                    ]
                )
            ],
        ),
    )
    return container


def build_rabbit_card_content(born_ts, strength, agility, intelligence, affection, satiation):
    birthday_str = (datetime.datetime.utcfromtimestamp(born_ts) + datetime.timedelta(hours=8)) \
        .strftime('%Y-%m-%d %H:%M:%S')
    img_url = 'https://obs.line-scdn.net/0h70H0wyxgaB91SUIJHCUXSEkMZnICZ25XDXh0KQIeMioMeXscGi8gfFceNi1eKXhMGSklfFBJNS9c'
    container = BubbleContainer(
        direction='ltr',
        hero=ImageComponent(
            url=img_url,
            size='full',
            aspect_ratio='20:15',
            aspect_mode='cover'
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(text='你的兔子（尚未取名）', weight='bold', size='xl'),
                SeparatorComponent(),
                BoxComponent(
                    layout='baseline',
                    margin='md',
                    contents=[
                        TextComponent(text=f'生日：{birthday_str}', size='sm', color='#999999', align='end')
                    ]
                ),
                BoxComponent(
                    layout='baseline',
                    margin='md',
                    contents=[
                        TextComponent(text=f'力量：{strength}', size='md', color='#000000'),
                        TextComponent(text='肌肉多多', size='sm', color='#999999', align='end')
                    ]
                ),
                BoxComponent(
                    layout='baseline',
                    margin='md',
                    contents=[
                        TextComponent(text=f'敏捷：{agility}', size='md', color='#000000'),
                        TextComponent(text='跳得很快', size='sm', color='#999999', align='end')
                    ]
                ),
                BoxComponent(
                    layout='baseline',
                    margin='md',
                    contents=[
                        TextComponent(text=f'智慧：{intelligence}', size='md', color='#000000'),
                        TextComponent(text='很會栽贓', size='sm', color='#999999', align='end')
                    ]
                ),
                BoxComponent(
                    layout='baseline',
                    margin='md',
                    contents=[
                        TextComponent(text=f'好感：{affection}', size='md', color='#000000'),
                        TextComponent(text='跟你多熟', size='sm', color='#999999', align='end')
                    ]
                ),
                BoxComponent(
                    layout='baseline',
                    margin='md',
                    contents=[
                        TextComponent(text=f'飽食：{satiation}', size='md', color='#000000'),
                        TextComponent(text='肚子多重', size='sm', color='#999999', align='end')
                    ]
                ),
            ],
        ),
        footer=BoxComponent(
            layout='horizontal',
            spacing='sm',
            contents=[
                ButtonComponent(
                    style='primary',
                    height='sm',
                    color='#95B9B4',
                    action=MessageAction(label='狀態', text='狀態（暫無功能）'),
                ),
                ButtonComponent(
                    style='primary',
                    height='sm',
                    color='#95B9B4',
                    action=MessageAction(label='找朽咪', text='找朽咪')
                ),
                ButtonComponent(
                    style='primary',
                    height='sm',
                    color='#95B9B4',
                    action=MessageAction(label='摸朽咪', text='摸朽咪')
                )
            ]
        ),
    )
    return container
