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
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# A simple "front door" that confirms the backend is alive and responding.
@app.get("/")
def health_check():
    return {"status": "backend is running"}

# Accepts a location reading, saves it to the database, and confirms receipt.
@app.post("/location")
def receive_location(animal_id: str, latitude: float, longitude: float):
    conn.execute(
        "INSERT INTO locations (animal_id, latitude, longitude, timestamp) VALUES (?, ?, ?, datetime('now'))",
        (animal_id, latitude, longitude)
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