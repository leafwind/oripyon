import datetime
import sqlite3
import time
from contextlib import closing

import cachetools.func
from linebot.models import (
    ConfirmTemplate, MessageAction, TemplateSendMessage
)

from app.utils.sqlite_util import table_exists
from constants import LINE_DB_PATH, TABLE_RABBIT_FEEDING


@cachetools.func.ttl_cache(ttl=86400)
def my_rabbit_exists(uid):
    with closing(sqlite3.connect(LINE_DB_PATH)) as conn, closing(conn.cursor()) as c:
        query = f"SELECT count(1) FROM {TABLE_RABBIT_FEEDING} WHERE uid=:uid;"
        c.execute(query, {'uid': uid})
        (count,) = c.fetchone()
    if count > 0:
        return True
    else:
        return False


def adopt_rabbit(uid):
    if my_rabbit_exists(uid):
        return [('text', '你已經有一隻兔子啦')]
    else:
        with closing(sqlite3.connect(LINE_DB_PATH)) as conn, closing(conn.cursor()) as c:
            now = int(time.time())
            insert_sql = f'''
                INSERT INTO {TABLE_RABBIT_FEEDING} VALUES (:uid, :born_ts);
            '''
            c.execute(insert_sql, {'uid': uid, 'born_ts': now})
            c.commit()
        time_str = (datetime.datetime.utcfromtimestamp(now) + datetime.timedelta(hours=8))\
            .strftime('%Y-%m-%d %H:%M:%S')
        return [('text', f'已經領養完畢，他的出生時間是 {time_str}')]


def my_rabbit(uid):
    if not table_exists(TABLE_RABBIT_FEEDING):
        check_or_create_table_rabbit_feeding()

    if not my_rabbit_exists(uid):
        actions = [
            MessageAction(
                label='領養兔子',
                text='領養兔子'
            ),
            MessageAction(
                label='沒事了',
                text='沒事了'
            )
        ]
        return [('flex', TemplateSendMessage(
            alt_text='請到手機確認是否領養',
            template=ConfirmTemplate(text='你還沒有兔子', actions=actions))
        )]
    else:
        return [('text', f'你的兔子資訊：')]


def check_or_create_table_rabbit_feeding():
    with closing(sqlite3.connect(LINE_DB_PATH)) as conn, closing(conn.cursor()) as c:
        create_sql = f'''
            CREATE TABLE IF NOT EXISTS {TABLE_RABBIT_FEEDING}
            (
                uid text,
                born_ts int,
                PRIMARY KEY (uid)
            )
        '''
        c.execute(create_sql)
        c.commit()


def insert_rabbit_feeding(uid):
    with closing(sqlite3.connect(LINE_DB_PATH)) as conn, closing(conn.cursor()) as c:
        insert_sql = f'''
            INSERT OR REPLACE INTO {TABLE_RABBIT_FEEDING} VALUES (:uid, :born_ts);
        '''
        c.execute(insert_sql, {'uid': uid, 'born_ts': int(time.time())})
        c.commit()
