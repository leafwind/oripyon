import sqlite3

from constants import LINE_DB_PATH, TABLE_LINE_ANNOUNCEMENT_LOG


def check_or_create_table_line_announcement_log():
    conn = sqlite3.connect(LINE_DB_PATH)
    c = conn.cursor()

    create_sql = f'''
        CREATE TABLE IF NOT EXISTS {TABLE_LINE_ANNOUNCEMENT_LOG}
        (
            group_id text, ts int,
            PRIMARY KEY (group_id, ts)
        )
    '''
    c.execute(create_sql)
    conn.commit()
    conn.close()


def insert_line_announcement_log(group_id, ts):
    conn = sqlite3.connect(LINE_DB_PATH)
    c = conn.cursor()
    insert_sql = f'''
        INSERT OR REPLACE INTO {TABLE_LINE_ANNOUNCEMENT_LOG} VALUES (:group_id, :ts);
    '''
    c.execute(insert_sql, {'group_id': group_id, 'ts': ts})
    conn.commit()
    conn.close()


def query_line_announcement_log(group_id):
    conn = sqlite3.connect(LINE_DB_PATH)
    c = conn.cursor()
    query_sql = f'''
        SELECT MAX(ts) AS max_ts FROM {TABLE_LINE_ANNOUNCEMENT_LOG}
        WHERE group_id=:group_id
    '''
    c.execute(query_sql, {'group_id': group_id})
    (max_ts,) = c.fetchone()
    max_ts = int(max_ts) if max_ts else 0
    conn.commit()
    conn.close()
    return max_ts
