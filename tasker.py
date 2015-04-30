#!/usr/bin/env python2

import sqlite3
import sys

# Path to Tasker DB
DB_PATH = "/home/aww/tasker.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tasker (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)")
connection.commit()
if len(sys.argv) > 1:
    if sys.argv[1] in ["add", "a", "new", "create"]:
        cursor.execute('INSERT INTO tasker (name, description) VALUES ("%s", "%s")' \
            % (sys.argv[2], ' '.join(sys.argv[3:])))
        print("Task: %s added!" % sys.argv[2])
        connection.commit()
    if sys.argv[1] in ["remove", "delete", "del", "rem"]:
        cursor.execute("DELETE FROM tasker WHERE id LIKE %i" % int(sys.argv[2]))
        print("Task %i was removed" % int(sys.argv[2]))
        connection.commit()
    if sys.argv[1] in ["purge", "remove_all", "fuckit"]:
        if str(raw_input("Are you sure you want to delete all your task?: ")) in ["y", "yes", "fuck yes"]:
            cursor.execute("DROP TABLE tasker")
            print("The evil has been purged.")
else:
    for row in cursor.execute("SELECT * FROM tasker"):
        id, name, description = row
        print("[%i] %s: %s" % (id, name, description))

