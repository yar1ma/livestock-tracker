# Brings in the tool that lets this script send data over the web.
import requests

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

    response = requests.post(
        "http://127.0.0.1:8000/location",
        params={"animal_id": "cow001", "latitude": latitude, "longitude": longitude}
    )
    print(response.json())
    time.sleep(5)