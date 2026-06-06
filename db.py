import sqlite3
from datetime import datetime

DB_NAME = "nasa_tracker.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row #access column by name instead of index
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    #Astronomy pictures
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS apod (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            title TEXT,
            explanation TEXT,
            url TEXT,
            media_type TEXT,
            fetched_at TEXT
       ) 
    """)

    #Near Earth Asteroids
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asteroids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nasa_id TEXT UNIQUE,
            name TEXT,
            estimated_diameter_min_km REAL,
            estimated_diameter_max_km REAL,
            is_potentially_hazardous INTEGER,
            close_approach_date TEXT,
            miss_distance_km REAL,
            relative_velocity_kmh REAL,
            fetched_at TEXT
        )
    """)

    # Mars Rover Photos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mars_photos (               
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_id INTEGER UNIQUE,
            sol INTEGER,
            earth_data TEXT,
            rover_name TEXT,
            camera_name TEXT,
            img_src TEXT,
            fetched_at TEXT
    """)

    conn.commit()
    conn.close()
    print("Database and tables ready")

    #APOD helper functions
    def insert_apod(data: dict):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO apod ( date, title, explanation, url, media_type, fetched_at ) 
                VALUES ( ?, ?, ?, ?, ?, ? )             
            """, (
                data['date'],
                data['title'],
                data['explanation'],
                data['url'],
                data['media_type'],
                datetime.now().isoformat()
            ))
            conn.commit()
        finally:
            conn.close()