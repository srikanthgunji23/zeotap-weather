import sqlite3

DATABASE_NAME = 'weather_data.db'

def create_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            date TEXT PRIMARY KEY,
            average_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_daily_summary(summary):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO daily_summary (date, average_temp, max_temp, min_temp, dominant_condition)
        VALUES (?, ?, ?, ?, ?)
    ''', (summary['date'], summary['average_temp'], summary['max_temp'], summary['min_temp'], summary['dominant_condition']))
    conn.commit()
    conn.close()
