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

def get_all_apod():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apod ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_asteroid(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO asteroids (
                        nasa_id, name, estimated_diameter_min_km, estimated_diameter_max_km,
                        is_potentially_hazardous, close_approach_date,
                        miss_distance_km, relative_velocity_kmh, fetched_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            data["nasa_id"],
            data["name"],
            data["estimated_diameter_min_km"],
            data["estimated_diameter_max_km"],
            data["is_potentially_hazardous"],
            data["close_approach_date"],
            data["miss_distance_km"],
            data["relative_velocity_kmh"],
            datetime.now().isoformat()
        ))
        conn.commit()
    finally:
        conn.close()

def get_all_asteroids():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM asteroids ORDER BY close_approach_date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def insert_mars_photo(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO mars_photos (
                photo_id, sol, earth_date, rover_name, camera_name, img_src, fetched_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["photo_id"],
            data["sol"],
            data["earth_date"],
            data["rover_name"],
            data["camera_name"],
            data["img_src"],
            datetime.now().isoformat()
        ))
        conn.commit()
    finally:
        conn.close()

def get_all_mars_photos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mars_photos ORDER BY earth_date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows