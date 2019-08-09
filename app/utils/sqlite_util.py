import sqlite3

import cachetools.func

from constants import LINE_DB_PATH


@cachetools.func.ttl_cache(ttl=86400)
def table_exists(table_name):
    conn = sqlite3.connect(LINE_DB_PATH)
    c = conn.cursor()
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    c.execute(query)
    result = c.fetchall()
    if result:
        return True
    else:
        return False
