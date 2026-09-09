# Brings in the tool that lets this script send data over the web.
import requests

# Sends one fake location reading to our backend's /location door.
response = requests.post(
    "http://127.0.0.1:8000/location",
    params={"animal_id": "cow001", "latitude": 5.6037, "longitude": -0.1870}
)
print(response.json())