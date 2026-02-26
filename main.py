import datetime
from numpy import ndarray, float64
from skyfield.api import load, wgs84
from skyfield import vectorlib, timelib, units


class Observer:
    PLANETS_TO_LOAD = [
        "mercury",
        "venus",
        "mars",
        "jupiter barycenter",
        "saturn barycenter",
        "uranus barycenter",
        "neptune barycenter",
    ]

    def __init__(self, latitude: float, longitude: float) -> None:
        self.ts = load.timescale()
        self.planets = load("de421.bsp")
        self.earth = self.planets["earth"]
        self.loaded_planets = {
            planet_name: self.planets[planet_name]
            for planet_name in self.PLANETS_TO_LOAD
        }
        self.latitude = latitude
        self.longitude = longitude
        self.location = self.earth + wgs84.latlon(latitude, longitude)

    def find_radec(
        self,
        planet: vectorlib.VectorSum,
        t: timelib.Time,
    ) -> tuple[units.Angle, units.Angle, units.Distance]:
        astrometric = self.location.at(t).observe(planet)
        ra, dec, distance = astrometric.radec()
        return (ra, dec, distance)

    def altaz(
        self,
        planet: string,
        t: timelib.Time,
    ) -> tuple[float64, float64, float64]:
        planet = self.loaded_planets[planet]
        apparent = self.location.at(t).observe(planet).apparent()
        alt, az, dist = apparent.altaz()
        return (alt.degrees, az.degrees, dist.au)


observer = Observer(42.42, 23.20)

t = observer.ts.from_datetime(
    datetime.datetime(2026, 2, 25, 21, 39, 00, 00, datetime.timezone.utc)
)

print(observer.altaz("mars", t))
