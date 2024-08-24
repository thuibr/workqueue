import sqlite3

con = sqlite3.connect("queue.db")
cur = con.cursor()
cur.execute("DROP TABLE queue")
cur.execute("CREATE TABLE IF NOT EXISTS queue(id INTEGER NOT NULL PRIMARY KEY, name, args, kwargs, running)")
con.commit()

