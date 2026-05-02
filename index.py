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

# ADD NEW COLUMNS TO USERS TABLE
try:
    cur.execute("ALTER TABLE users ADD COLUMN fullname TEXT")
except:
    pass

try:
    cur.execute("ALTER TABLE users ADD COLUMN organization TEXT")
except:
    pass

try:
    cur.execute("ALTER TABLE users ADD COLUMN phone TEXT")
except:
    pass

try:
    cur.execute("ALTER TABLE users ADD COLUMN city TEXT")
except:
    pass
cur.execute("DELETE FROM users")


# FOOD TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    quantity TEXT NOT NULL,
    location TEXT NOT NULL
)
""")

# REQUESTS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    quantity TEXT,
    location TEXT,
    status TEXT
)
""")


cur.execute("""
INSERT OR IGNORE INTO users (fullname, organization, email, phone, city, role, password)
VALUES ('Rest User','Hotel ABC','rest1@gmail.com','9999999999','Bhopal','restaurant','1234')
""")

cur.execute("""
INSERT OR IGNORE INTO users (fullname, organization, email, phone, city, role, password)
VALUES ('NGO User','Helping NGO','ngo1@gmail.com','8888888888','Bhopal','ngo','123')
""")

cur.execute("""
INSERT OR IGNORE INTO users (fullname, organization, email, phone, city, role, password)
VALUES ('Admin','System','admin@gmail.com','7777777777','Bhopal','admin','12345')
""")
# check tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", cur.fetchall())

conn.commit()
conn.close()