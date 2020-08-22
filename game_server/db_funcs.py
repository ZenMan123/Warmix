import sqlite3
from hashlib import md5

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()


def register(login: str, password: str, name: str):
    password = md5(bytes(password, encoding='utf-8')).hexdigest()
    try:
        cur.execute("""insert into users(login, password, name) VALUES (?, ?, ?);""", (login, password, name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print('login error')
        return False


def login(login: str, password: str):
    password = md5(bytes(password, encoding='utf-8')).hexdigest()
    res = cur.execute("""SELECT * FROM users WHERE login=?""", (login,)).fetchone()
    if res[2] == password:
        return res
    return None



