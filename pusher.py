import json
import sqlite3

con = sqlite3.connect("queue.db")

cur = con.cursor()

name = 'hello'
running = 0
args = ['tom']
kwargs = {"all_caps": True}

args = json.dumps(args)
kwargs = json.dumps(kwargs)

cur.execute("INSERT INTO queue(name, running, args, kwargs) values (?,?,?,?)", (name, running, args, kwargs))

con.commit()
