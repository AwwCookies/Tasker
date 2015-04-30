#!/usr/bin/env python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Author: Emma Jones (AwwCookies)                                           #
#   Last Update: Apr 30 2015                                              # # #
#   Version: 1.0                                                          # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import sqlite3
import sys

# Path to Tasker DB
DB_PATH = "/home/aww/tasker.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Create a new table in the database if one does not exists with three cols
cursor.execute("CREATE TABLE IF NOT EXISTS tasker (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)")
# This saves the changes to the database
connection.commit()
# $ tasker
if len(sys.argv) > 1:
    # $ tasker add Cookies go buy cookies
    if sys.argv[1] in ["add", "a", "new", "create"]:
        cursor.execute('INSERT INTO tasker (name, description) VALUES ("%s", "%s")'
                       % (sys.argv[2], ' '.join(sys.argv[3:])))
        print("Task: %s added!" % sys.argv[2])
        connection.commit()
    # $ tasker remove 1
    if sys.argv[1] in ["remove", "delete", "del", "rem"]:
        cursor.execute("DELETE FROM tasker WHERE id LIKE %i" % int(sys.argv[2]))
        #TODO Find a better way of reindexing the table
        rows = []
        for id, name, desc in cursor.execute("SELECT * FROM tasker"):
            rows.append((id, name, desc))
        cursor.execute("DROP TABLE tasker")
        cursor.execute('CREATE TABLE  tasker (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)')
        for row in rows:
            cursor.execute('INSERT INTO tasker (name, description) VALUES ("%s", "%s")'% (row[1], row[2]))

        print("Task %i was removed" % int(sys.argv[2]))
        connection.commit()
    if sys.argv[1] in ["purge", "remove_all", "fuckit"]:
        if str(raw_input("Are you sure you want to delete all your task?: ")) in ["y", "yes", "fuck yes"]:
            cursor.execute("DROP TABLE tasker")
            print("The evil has been purged.")
    if sys.argv[1] in ["help", "wtf"]:
        pass
else:
    for id, name, description in cursor.execute("SELECT * FROM tasker"):
        print("[%i] %s: %s" % (id, name, description))
