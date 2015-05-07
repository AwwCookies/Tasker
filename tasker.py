#!/usr/bin/env python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Author: Emma Jones (AwwCookies)                                           #
#   Last Update: May 06 2015                                              # # #
#   Version: 3.0                                                          # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sqlite3
import json
import sys
import urllib.request
import os

from prettytable import PrettyTable

# CONFIG
DB_PATH = "/home/aww/"
UPDATE_URL = "https://raw.githubusercontent.com/AwwCookies/Tasker/master/tasker.py"

connection = sqlite3.connect(DB_PATH + "tasker.db")
cursor = connection.cursor()

# Create a new table in the database if one does not exists with three cols
cursor.execute(
    "CREATE TABLE IF NOT EXISTS tasker (ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)")
# This saves the changes to the database
connection.commit()

def strikethrough(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])


def export_csv(cursor):
    for ID, name, desc in cursor.execute("SELECT * FROM tasker"):
        print("%s, %s, %s" % (ID, name, desc))


def export_json(cursor):
    db = dict()
    for ID, name, desc in cursor.execute("SELECT * FROM tasker"):
        db[ID] = {"ID": ID, "name": name, "desc": desc}
    print(json.dumps(db))


def import_csv(cursor, file_path):
    with open(file_path, 'r') as csv:
        for line in csv.readlines():
            name = line.split(',')[1].strip()
            desc = ' '.join(line.split(',')[2:]).strip()
            cursor.execute(
                'INSERT INTO tasker (name, description) VALUES ("%s", "%s")' % (name, desc))
            print("Task: %s added!" % name)


def import_json(cursor, file_path):
    db = json.loads(open(file_path).read())
    for key in db.keys():
        cursor.execute(
            'INSERT INTO tasker (name, description) VALUES ("%s", "%s")' % (
                db[key]["name"], db[key]["desc"]))
        print("Task: %s added!" % db[key]["name"])


def update():
    ud = urllib.request.urlopen(UPDATE_URL).read().decode('utf-8')
    with open("/tmp/tasker.py", 'w') as updated_file:
        updated_file.write(str(ud))
    os.system("sudo mv /tmp/tasker.py /usr/bin/tasker")
    os.system("sudo chmod +777 /usr/bin/tasker")

# $ tasker
if len(sys.argv) > 1:
    sys.argv[1] = sys.argv[1].lower()
    # $ tasker add Cookies go buy cookies
    if sys.argv[1] in ["add", "a", "new", "create"]:
        cursor.execute('INSERT INTO tasker (name, description) VALUES ("%s", "%s")'
                       % (sys.argv[2], ' '.join(sys.argv[3:])))
        print("Task: %s added!" % sys.argv[2])
        connection.commit()
    # $ tasker remove 1
    if sys.argv[1] in ["remove", "delete", "del", "rem"]:
        cursor.execute("DELETE FROM tasker WHERE ID LIKE %i" %
                       int(sys.argv[2]))
        # TODO Find a better way of reindexing the table
        rows = []
        for ID, name, desc in cursor.execute("SELECT * FROM tasker"):
            rows.append((ID, name, desc))
        cursor.execute("DROP TABLE tasker")
        cursor.execute(
            'CREATE TABLE  tasker (ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)')
        for row in rows:
            cursor.execute(
                'INSERT INTO tasker (name, description) VALUES ("%s", "%s")' % (row[1], row[2]))

        print("Task %i was removed" % int(sys.argv[2]))
        connection.commit()
    if sys.argv[1] in ["purge", "remove_all", "fuckit"]:
        if str(input("Are you sure you want to delete all your task?: ")) in ["y", "yes", "fuck yes"]:
            cursor.execute("DROP TABLE tasker")
            print("The evil has been purged.")
    if sys.argv[1] in ["help", "wtf"]:
        pass
    if sys.argv[1] == "export":
        if sys.argv[2] == "csv":
            export_csv(cursor)
        elif sys.argv[2] == "json":
            export_json(cursor)
    if sys.argv[1] == "update":
        update()
        print("Update complete")
    if sys.argv[1] == "import":
        if sys.argv[2] == "csv":
            import_csv(cursor, sys.argv[3])
            connection.commit()
        if sys.argv[2] == "json":
            import_json(cursor, sys.argv[3])
            connection.commit()
    if sys.argv[1] in ["complete", "done", "cross", "x"]:
        for row in cursor.execute("SELECT * FROM tasker WHERE ID LIKE %i" % int(sys.argv[2])):
            cursor.execute('UPDATE tasker SET name=?, description=? WHERE ID=?', (strikethrough(row[1]), strikethrough(row[2]), int(sys.argv[2])))
        connection.commit()
else:
    table = PrettyTable(encoding=None)
    table.field_names = ['ID', "Name", "Description"]
    for ID, name, desc in cursor.execute("SELECT * FROM tasker"):
        table.add_row([ID, name, desc])
    print(table.get_string())