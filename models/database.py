import sqlite3
from flask import g
import os

DATABASE = os.path.join(os.getcwd(), 'finance.db')
                        
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):

    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
def init_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   email TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
                   """)

    conn.commit()
    conn.close()
