import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

# USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# FOOD TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    quantity TEXT NOT NULL,
    location TEXT NOT NULL
)
""")

# REQUEST TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    quantity TEXT,
    location TEXT,
    status TEXT
)
""")

# demo users
cur.execute("INSERT OR IGNORE INTO users (email, password, role) VALUES ('rest1@gmail.com','1234','restaurant')")
cur.execute("INSERT OR IGNORE INTO users (email, password, role) VALUES ('ngo1@gmail.com','123','ngo')")
cur.execute("INSERT OR IGNORE INTO users (email, password, role) VALUES ('admin@gmail.com','12345','admin')")

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()

print("Tables in DB:", tables)

conn.commit()
conn.close() 