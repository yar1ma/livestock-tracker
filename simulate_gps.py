# Brings in Python's own built-in tools for sending web requests, no extra install needed.
import urllib.request
import urllib.parse

# Brings in "time" so we can pause between each fake reading.
import time

# Brings in "random" so we can generate small random movements.
import random

# Starting position for our fake cow, near Accra as an example.
latitude = 5.6037
longitude = -0.1870

# Repeats forever, moving slightly and sending a new reading every 5 seconds.
while True:
    latitude += random.uniform(-0.0005, 0.0005)
    longitude += random.uniform(-0.0005, 0.0005)

    params = urllib.parse.urlencode({
        "animal_id": "cow001",
        "latitude": latitude,
        "longitude": longitude
    })
    url = f"http://127.0.0.1:8000/location?{params}"

    response = urllib.request.urlopen(url, data=b"")
    print(response.read().decode())

    time.sleep(5)