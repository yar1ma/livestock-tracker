from fastapi import FastAPI
import sqlite3
app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "backend is running"}

@app.post("/location")
def receive_location(animal_id: str, latitude: float, longitude: float):
    print(f"Animal {animal_id} is at {latitude}, {longitude}")
    return {"status": "received"}