import requests

url = "https://nominatim.openstreetmap.org/search"
headers = {"User-Agent": "my-geocoding-app/1.0 (your@email.com)"}


def city_geoposition(city_name: str) -> tuple[float, float] | None:
    params = {"q": city_name, "format": "json", "limit": 1}
    try:
        response = requests.get(url=url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None
        longitude = float(data[0]["lon"])
        latitude = float(data[0]["lat"])
        return (latitude, longitude)
    except requests.RequestException:
        return None
