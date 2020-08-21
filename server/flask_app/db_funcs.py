import sqlite3

conn = sqlite3.connect("db.sqlite")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()



