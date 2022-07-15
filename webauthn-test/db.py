import os
import sqlite3

FILENAME = 'webauthn-test.db'

def _get_db_conn():
    """Makes a connection to the database"""

    # connect to database
    _db_conn = sqlite3.connect(FILENAME)
    _db_conn.row_factory = sqlite3.Row
    return _db_conn

def init_db():
    if not os.path.exists(FILENAME):
        with _get_db_conn() as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                credential_id BLOB,
                credential_public_key BLOB
            )''')

def make_new_user(
    username: str, 
    email: str,
    credential_id: bytes,
    credential_public_key: bytes
    ):
    with _get_db_conn() as conn:
        conn.execute('''
        INSERT INTO users (
            username, email, credential_id, credential_public_key
        ) VALUES (
            ?, ?, ?, ?
        )''', 
        (
            username, 
            email, 
            credential_id, 
            credential_public_key
        ))

def get_user_data(username: str):
    with _get_db_conn() as conn:
        return conn.execute('''
            SELECT * 
            FROM users 
            WHERE username = ?
            ''', 
            (
                username,
            )).fetchone()

def delete_user(username: str):
    with _get_db_conn() as conn:
        conn.execute('''
            DELETE FROM users
            WHERE username = ?
            ''', 
            (
                username,
            ))