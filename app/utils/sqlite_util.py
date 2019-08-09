import sqlite3
from contextlib import closing

import cachetools.func

from constants import LINE_DB_PATH


@cachetools.func.ttl_cache(ttl=86400)
def table_exists(table_name):
    with closing(sqlite3.connect(LINE_DB_PATH)) as conn, closing(conn.cursor()) as c:
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        c.execute(query)
        result = c.fetchall()
    if result:
        return True
    else:
        return False
