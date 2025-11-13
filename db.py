import sqlite3
import os

# Get the absolute path of the folder this 'db.py' file is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create the full path for the database file, putting it right next to db.py
DB_PATH = os.path.join(BASE_DIR, "duty_system.db")

def get_connection():
    # Connect using the new, absolute path
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        studentIDNumber TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        course TEXT NOT NULL,
        contactNumber TEXT NOT NULL,
        password TEXT NOT NULL,
        userRole TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Events (
        eventID INTEGER PRIMARY KEY AUTOINCREMENT,
        eventDate TEXT NOT NULL,
        eventName TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

# --- IMPORTANT ---
# Delete this line if it's at the bottom of your file.
# It's now called from system.py and main.py, which is better.
# initialize_db()