import sqlite3
import hashlib


conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()


def login(login, password):
    cur.execute("""
        SELECT * FROM users where login = ?;
    """, (login, ))
    res = cur.fetchone()
    if res and res[2] == hashlib.md5(bytes(password, encoding='utf-8')).hexdigest():
        return res
    return None


def register(login, password, name):
    password = hashlib.md5(bytes(password, encoding='utf-8')).hexdigest()
    cur.execute("""
        INSERT INTO users(login, password, name, rating) VALUES (?, ?, ?, 0);
    """, (login, password, name))
    conn.commit()


register('zenman', '123', 'Artem')
print(login('zenman', '123'))



