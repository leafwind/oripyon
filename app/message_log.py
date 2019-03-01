import logging
import sqlite3
import time

from constants import LINE_DB_PATH, TABLE_LINE_CMD_COUNT


def check_or_create_table_line_cmd_count():
    conn = sqlite3.connect(LINE_DB_PATH)
    c = conn.cursor()

    create_sql = f'''
        CREATE TABLE IF NOT EXISTS {TABLE_LINE_CMD_COUNT}
        (
            group_id text, user_id text, cmd text, ts int,
            PRIMARY KEY (group_id, user_id, cmd, ts)
        )
    '''.format(TABLE_LINE_CMD_COUNT=TABLE_LINE_CMD_COUNT)

    logging.info(create_sql)
    c.execute(create_sql)
    conn.commit()
    conn.close()


def insert_line_cmd_count(group_id, user_id, cmd, ts):
    conn = sqlite3.connect(LINE_DB_PATH)
    c = conn.cursor()
    insert_sql = f'''
        INSERT OR REPLACE INTO {TABLE_LINE_CMD_COUNT} VALUES (\':group_id\', \':user_id\', \':cmd\', :ts);
    '''.format(TABLE_LINE_CMD_COUNT=TABLE_LINE_CMD_COUNT)
    logging.info(insert_sql)
    c.execute(insert_sql, {'group_id': group_id, 'user_id': user_id, 'cmd': cmd, 'ts': ts})
    conn.commit()
    conn.close()


def query_line_cmd_count(group_id, user_id, cmd, date_line_diff_ts=-4*3600):
    conn = sqlite3.connect(LINE_DB_PATH)
    c = conn.cursor()
    now = int(time.time())
    today_ts_till_now = (now - date_line_diff_ts) % 86400
    last_date_line_ts = now - today_ts_till_now
    query_sql = f'''
        SELECT COUNT(1) AS count FROM {TABLE_LINE_CMD_COUNT}
        WHERE group_id=\':group_id\' AND user_id=\':user_id\' AND cmd=\':cmd\' AND ts>:last_date_line_ts
    '''.format(TABLE_LINE_CMD_COUNT=TABLE_LINE_CMD_COUNT)
    logging.info(f'''
        SELECT COUNT(1) AS count FROM {TABLE_LINE_CMD_COUNT}
        WHERE group_id=\'{group_id}\' AND user_id=\'{user_id}\' AND cmd=\'{cmd}\' AND ts>{last_date_line_ts}''')
    c.execute(query_sql,
              {'group_id': group_id,
               'user_id': user_id,
               'cmd': cmd,
               'last_date_line_ts': last_date_line_ts})
    (count,) = c.fetchone()
    count = int(count) if count else 0
    conn.commit()
    conn.close()
    return count