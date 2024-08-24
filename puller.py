import json
import sqlite3

import tasks

DATABASE = "queue.db"

con = sqlite3.connect(DATABASE)
cur = con.cursor()

while True:
    try:
        con.execute("BEGIN TRANSACTION")

        cur.execute("SELECT id, name, args, kwargs FROM queue WHERE running = 0 LIMIT 1")
        row = cur.fetchone()

        if row is None:
            con.execute("ROLLBACK")
            continue

        _id, name, args, kwargs = row
        args = json.loads(args)
        kwargs = json.loads(kwargs)

        cur.execute("UPDATE queue SET running = 1 WHERE id = ?", (_id,))

        if cur.rowcount == 0:
            # Row was modified by another process
            # Rollback and continue
            con.execute("ROLLBACK")
            continue

        con.commit()

        task = getattr(tasks, name)
        task(*args, **kwargs)

        con.execute("UPDATE queue SET running = 2 WHERE id = ?", (_id,))
        con.commit()

    except sqlite3.OperationalError:
        con.execute("ROLLBACK")
    except Exception as e:
        con.execute("ROLLBACK")
        print(f"Error processing queue: {e}")


