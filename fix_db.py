import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# DROP and recreate (nuclear option)
cursor.execute("DROP TABLE IF EXISTS expenses")
cursor.execute("DROP TABLE IF EXISTS categories")

# Create FRESH tables
cursor.execute("""
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category_id INTEGER,
        date TEXT NOT NULL,
        note TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
""")

# Add categories
categories = [('Food',), ('Transport',), ('Entertainment',), ('Shopping',), ('Bills',)]
cursor.executemany("INSERT INTO categories (category_name) VALUES (?)", categories)

conn.commit()
conn.close()
print("✅ TABLES FIXED! Run app now!")
