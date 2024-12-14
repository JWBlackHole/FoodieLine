import sqlite3

DATABASE = "locations.db"

def get_db_connection():
    conn             = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Initialize the database and create the table if it doesn't exist
    conn   = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        latitude REAL,
        longitude REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def get_user_location(user_id: str) -> dict:
    conn   = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT user_id, latitude, longitude, timestamp
    FROM user_locations
    WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        location = {
            "status"   : "Ok",
            "user_id"  : row["user_id"],
            "latitude" : row["latitude"],
            "longitude": row["longitude"],
            "timestamp": row["timestamp"]
        }
        return location
    else:
        return {"status": "Not Found"}
    
def user_has_locations(user_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM user_locations WHERE user_id = ? LIMIT 1", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
    
def add_user_location(user_id: str, latitude: float, longitude: float) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()

    if user_has_locations(user_id):
        # If the user already has a location stored, update it
        cursor.execute("""
        UPDATE user_locations
        SET latitude = ?, longitude = ?, timestamp = CURRENT_TIMESTAMP
        WHERE user_id = ?
        """, (latitude, longitude, user_id))
        message = "Location updated"
    else:
        # If the user does not have a location, insert a new record
        cursor.execute("""
        INSERT INTO user_locations (user_id, latitude, longitude)
        VALUES (?, ?, ?)
        """, (user_id, latitude, longitude))
        message = "Location recorded"

    conn.commit()
    conn.close()
    
    print(message)

    return {"status": message}