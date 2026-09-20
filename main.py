# Brings in FastAPI's tools so we can build our backend with them.
from fastapi import FastAPI

# Lets our React dashboard (running on a different port) talk to this backend.
from fastapi.middleware.cors import CORSMiddleware

# Brings in SQLite, Python's built-in tool for talking to a simple database.
import sqlite3

# Creates our backend application, the base everything else attaches to.
app = FastAPI()

# Allows requests from our dashboard's address, which browsers block by default.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# The center point and radius of our grazing boundary, in meters.
BOUNDARY_LAT = 5.6037
BOUNDARY_LON = -0.1870
BOUNDARY_RADIUS = 200

# Calculates distance in meters between two GPS points, same formula as the dashboard.
import math

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Connects to (or creates) a database file called "locations.db".
conn = sqlite3.connect("locations.db", check_same_thread=False)

# Creates a table to store animal ID, position, and time for each reading.
conn.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_id TEXT,
        latitude REAL,
        longitude REAL,
        timestamp TEXT
    )
""")

# Creates a table to record every time the animal crosses the boundary.
conn.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_id TEXT,
        message TEXT,
        timestamp TEXT
    )
""")

# A simple "front door" that confirms the backend is alive and responding.
@app.get("/")
def health_check():
    return {"status": "backend is running"}

# Accepts a location reading, saves it, checks the boundary, and logs an alert if crossed.
@app.post("/location")
def receive_location(animal_id: str, latitude: float, longitude: float):
    conn.execute(
        "INSERT INTO locations (animal_id, latitude, longitude, timestamp) VALUES (?, ?, ?, datetime('now'))",
        (animal_id, latitude, longitude)
    )
    conn.commit()

    distance = get_distance(BOUNDARY_LAT, BOUNDARY_LON, latitude, longitude)
    if distance > BOUNDARY_RADIUS:
        conn.execute(
            "INSERT INTO alerts (animal_id, message, timestamp) VALUES (?, ?, datetime('now'))",
            (animal_id, f"{animal_id} has left its assigned grazing boundary")
        )
        conn.commit()

    return {"status": "saved"}

# Returns the most recent location for one specific animal.
@app.get("/location/{animal_id}")
def get_latest_location(animal_id: str):
    row = conn.execute(
        "SELECT latitude, longitude, timestamp FROM locations WHERE animal_id = ? ORDER BY id DESC LIMIT 1",
        (animal_id,)
    ).fetchone()
    return {"latitude": row[0], "longitude": row[1], "timestamp": row[2]}

# Returns the latest known location for every animal that has ever reported one.
@app.get("/locations")
def get_all_latest_locations():
    animal_ids = conn.execute("SELECT DISTINCT animal_id FROM locations").fetchall()
    results = []
    for (animal_id,) in animal_ids:
        row = conn.execute(
            "SELECT latitude, longitude, timestamp FROM locations WHERE animal_id = ? ORDER BY id DESC LIMIT 1",
            (animal_id,)
        ).fetchone()
        results.append({"animal_id": animal_id, "latitude": row[0], "longitude": row[1], "timestamp": row[2]})
    return results

# Returns every saved location for one specific animal, oldest to newest.
@app.get("/history/{animal_id}")
def get_location_history(animal_id: str):
    rows = conn.execute(
        "SELECT latitude, longitude, timestamp FROM locations WHERE animal_id = ? ORDER BY id ASC",
        (animal_id,)
    ).fetchall()
    return [{"latitude": r[0], "longitude": r[1], "timestamp": r[2]} for r in rows]