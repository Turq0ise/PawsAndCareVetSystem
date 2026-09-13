import sqlite3
import datetime
from modules.idGen import idGen

# 1. Connect to a database (creates 'example.db' file if it doesn't exist)
conn = sqlite3.connect('example.db')

# 2. Create a cursor object to execute SQL commands
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;") # to allow foreign keys

# 3. Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS owners (
        owner_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        contact_number TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        pet_id TEXT PRIMARY KEY,
        owner_id text REFERENCES owners(owner_id),
        name TEXT NOT NULL,
        species TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id TEXT PRIMARY KEY,
        pet_id TEXT REFERENCES pets(pet_id),
        reason TEXT,
        date TEXT,
        time TEXT,
        status TEXT
    )
''')

# 4. Insert data safely using placeholders (?) to prevent SQL injection
cursor.execute("INSERT INTO owners (owner_id, name, contact_number) VALUES (?, ?, ?)", (idGen("Joel Samaniego", "owner"), "Joel Samaniego", 213456))
# cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 25))

conn.commit()  # Save the changes

# 5. Query and fetch data
cursor.execute("SELECT * FROM owners")
rows = cursor.fetchall()

for row in rows:
    print(row)

# 6. Close the connection when finished
conn.close()
