import sqlite3

from constants import TG_USER_LOCATION_DB_PATH, TABLE_TG_USER_LOCATION


def check_or_create_table_tg_user_location():
    conn = sqlite3.connect(TG_USER_LOCATION_DB_PATH)
    c = conn.cursor()

    create_sql = f'''
        CREATE TABLE IF NOT EXISTS {TABLE_TG_USER_LOCATION}
        (
            user_id text, first_name text, user_name text, lat real, lon real,
            PRIMARY KEY (user_id)
        )
    '''
    c.execute(create_sql)
    conn.commit()
    conn.close()


def insert_tg_user_location(user_id, first_name, user_name, lat, lon):
    conn = sqlite3.connect(TG_USER_LOCATION_DB_PATH)
    c = conn.cursor()
    insert_sql = f'''
        INSERT OR REPLACE INTO {TABLE_TG_USER_LOCATION} VALUES (:user_id, :first_name, :user_name, :lat, :lon);
    '''
    c.execute(
        insert_sql, {
            'user_id': user_id, 'first_name': first_name, 'user_name': user_name, 'lat': lat, 'lon': lon
        }
    )
    conn.commit()
    conn.close()


def query_tg_user_location(user_id):
    conn = sqlite3.connect(TG_USER_LOCATION_DB_PATH)
    c = conn.cursor()
    query_sql = f'''
        SELECT lat, lon FROM {TABLE_TG_USER_LOCATION}
        WHERE user_id=:user_id
    '''
    c.execute(query_sql, {'user_id': user_id})
    gps_location = c.fetchone()
    conn.commit()
    conn.close()
    return gps_location
