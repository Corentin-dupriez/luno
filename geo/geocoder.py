import requests

url = "https://nominatim.openstreetmap.org/search"
headers = {"User-Agent": "my-geocoding-app/1.0 (your@email.com)"}


def city_geoposition(city_name: str) -> tuple[float, float]:
    params = {"q": city_name, "format": "json", "limit": 1}
    response = requests.get(url=url, params=params, headers=headers)
    parsed_response = response.json()[0]
    longitude = float(parsed_response["lon"])
    latitude = float(parsed_response["lat"])
    return (latitude, longitude)
