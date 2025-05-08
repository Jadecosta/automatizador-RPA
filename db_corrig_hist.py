import pandas as pd
import sqlite3

conn = sqlite3.connect('historico.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    operation_type TEXT,
    date_time TEXT,
    file_name TEXT,
    log_file_name TEXT,
    task_id TEXT
)
''')

conn.commit()
conn.close()
