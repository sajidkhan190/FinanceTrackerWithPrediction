import sqlite3
from flask import g
import os

DATABASE = os.path.join(os.getcwd(), 'finance_db.db')
                        
def get_db():
    db = getattar(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):

    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
        