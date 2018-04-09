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

# def search(title="",author="",year="",isbn=""):
#     conn = sqlite3.connect("books.db")
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM book WHERE title=? OR author =? OR year =? OR isbn=?",(title,author,year,isbn))
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def delete(id):
#     conn = sqlite3.connect("books.db")
#     cur = conn.cursor()
#     cur.execute("DELETE FROM book WHERE id=?",(id,))
#     conn.commit()
#     conn.close()

# def update(id,title,author,year,isbn):
#     conn = sqlite3.connect("books.db")
#     cur = conn.cursor()
#     cur.execute("UPDATE book SET title=? , author=?, year=?, isbn=? WHERE id=?",(title,author,year,isbn,id))
#     conn.commit()
#     conn.close()

# connect()
