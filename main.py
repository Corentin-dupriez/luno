import datetime
from numpy import ndarray
from skyfield.api import load, N, W, wgs84
from skyfield import vectorlib, timelib, units


def find_radec(
    latitude: float,
    longitude: float,
    planet: vectorlib.VectorSum | ndarray,
    t: timelib.Time,
) -> tuple[units.Angle, units.Angle, units.Distance]:
    city = find_city_location(latitude, longitude)
    astrometric = city.at(t).observe(planet)
    ra, dec, distance = astrometric.radec()
    return (ra, dec, distance)


def find_altazdist(
    latitude: float,
    longitude: float,
    planet: vectorlib.VectorSum | ndarray,
    earth: vectorlib.VectorSum | ndarray,
    t: timelib.Time,
) -> tuple[units.Angle, units.Angle, units.Distance]:
    city = find_city_location(latitude, longitude, earth)
    apparent = city.at(t).observe(planet).apparent()
    alt, az, dist = apparent.altaz()
    return (alt, az, dist)


def find_city_location(
    latitude: float, longitude: float, earth: vectorlib.VectorSum | ndarray
) -> vectorlib.VectorSum:
    return earth + wgs84.latlon(latitude * N, longitude * W)


class Observer:
    def __init__(self) -> None:
        self.ts = load.timescale()
        self.planets = load("de421.bsp")
        self.earth = self.planets["earth"]
        self.mars = self.planets["mars"]


observer = Observer()

t = observer.ts.from_datetime(
    datetime.datetime(2026, 2, 25, 21, 39, 00, 00, datetime.timezone.utc)
)

print(find_altazdist(42.42, 23.20, observer.mars, observer.earth, t))
