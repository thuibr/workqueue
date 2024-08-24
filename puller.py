import json
import sqlite3
import time

import tasks

WAIT_TIME = 0.1

con = sqlite3.connect("queue.db")
cur = con.cursor()

while True:
    try:
        con.execute("BEGIN TRANSACTION")

        # Get the first row to be put into the queue, ordered by id
        cur.execute("SELECT id, name, args, kwargs FROM queue WHERE running = 0 ORDER BY id LIMIT 1")
        row = cur.fetchone()

        if row is None:
            # No row available
            # Continue to the next iteration
            con.execute("ROLLBACK")
            time.sleep(WAIT_TIME)
            continue

        # Parse out the values of the row
        _id, name, args, kwargs = row
        # Here we are using JSON to serialize/deserialize the args and kwargs
        # since there isn't an sqlite3 data type that they naturally fit in
        args = json.loads(args)
        kwargs = json.loads(kwargs)

        # Let other workers know that we are working on this task
        cur.execute("UPDATE queue SET running = 1 WHERE id = ?", (_id,))

        if cur.rowcount == 0:
            # Another worker beat us to this row
            # Rollback and continue
            con.execute("ROLLBACK")
            time.sleep(WAIT_TIME)
            continue

        con.commit()

        # Finally, run the task
        task = getattr(tasks, name)
        task(*args, **kwargs)

        # Mark it complete
        con.execute("UPDATE queue SET running = 2 WHERE id = ?", (_id,))
        con.commit()

    except sqlite3.OperationalError:
        # Often, we get a database locked error here
        con.execute("ROLLBACK")
    except Exception as e:
        con.execute("ROLLBACK")
        print(f"Error processing queue: {e}")


