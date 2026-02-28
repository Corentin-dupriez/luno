import requests

url = "https://nominatim.openstreetmap.org/search"
params = {"q": "Sofia, Bulgaria", "format": "json", "limit": 1}

headers = {"User-Agent": "my-geocoding-app/1.0 (your@email.com)"}
response = requests.get(url=url, params=params, headers=headers)

print(response.json())
