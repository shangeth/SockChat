import sqlite3


def connect():
    conn = sqlite3.connect("messagedb.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messagetable(id INTEGER PRIMARY KEY, message text)")
    conn.commit()
    conn.close()

def insert(msg):
    connect()
    conn = sqlite3.connect("messagedb.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO messagetable VALUES(NULL,?)",(msg,))
    conn.commit()
    conn.close()

def view():
    connect()
    msg_list=[]
    conn = sqlite3.connect("messagedb.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM messagetable")
    rows = cur.fetchall()
    conn.close()
    for i in rows:
        msg_list.append(i[1])
    return msg_list


