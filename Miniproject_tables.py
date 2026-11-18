import sqlite3

connection=sqlite3.connect("Library.db")
cursor=connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")



cursor.execute("""
    CREATE TABLE IF NOT EXISTS BOOKS(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn  TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    available_copies INTEGER NOT NULL DEFAULT 1
    )
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS MEMBER(
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name  TEXT NOT NULL,
    last_name TEXT ,
    email TEXT NOT NULL,
    phone INTEGER NOT NULL,
    membership_status TEXT NOT NULL
    )
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS BORROW_HISTORY(
    tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id  INTEGER,
    member_id INTEGER ,
    member_name TEXT NOT NULL,
    title TEXT NOT NULL,
    borrow_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT "Borrowed",
    FOREIGN KEY (book_id) 
            REFERENCES BOOKS (book_id),
    FOREIGN KEY (member_id) 
            REFERENCES MEMBER (member_id)
    )
    """)
cursor.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)



connection.commit()
connection.close()








