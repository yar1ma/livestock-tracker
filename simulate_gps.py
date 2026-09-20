# Brings in Python's own built-in tools for sending web requests, no extra install needed.
import urllib.request
import urllib.parse

# Brings in "time" so we can pause between each fake reading.
import time

# Brings in "random" so we can generate small random movements.
import random

# Starting positions for three fake cows, each slightly apart from the others.
cows = {
    "cow001": {"lat": 5.6037, "lon": -0.1870},
    "cow002": {"lat": 5.6050, "lon": -0.1880},
    "cow003": {"lat": 5.6020, "lon": -0.1860},
}

# Repeats forever, moving each cow slightly and sending a new reading every 5 seconds.
while True:
    for animal_id, pos in cows.items():
        pos["lat"] += random.uniform(-0.0005, 0.0005)
        pos["lon"] += random.uniform(-0.0005, 0.0005)

        params = urllib.parse.urlencode({
            "animal_id": animal_id,
            "latitude": pos["lat"],
            "longitude": pos["lon"]
        })
        url = f"http://127.0.0.1:8000/location?{params}"

        response = urllib.request.urlopen(url, data=b"")
        print(response.read().decode())

    time.sleep(5)