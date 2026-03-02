import datetime
from numpy import float64
from skyfield.api import load, wgs84
from skyfield import timelib, units
from dataclasses import dataclass


@dataclass
class Observation:
    planet_name: str
    altitude_deg: float
    azimuth_deg: float
    distance_au: float
    visible: bool
    rating: int = 0


class Observer:
    PLANETS_TO_LOAD = {
        "mercury": "mercury",
        "venus": "venus",
        "mars": "mars",
        "jupiter": "jupiter barycenter",
        "saturn": "saturn barycenter",
        "uranus": "uranus barycenter",
        "neptune": "neptune barycenter",
    }

    VISUAL_MAGNITUDE = {
        "Venus": -4,
        "Jupiter": -2.2,
        "Mercury": -2.5,
        "Mars": -2.9,
        "Saturn": -0.5,
        "Uranus": 5.7,
        "Neptune": 7.8,
    }

    def __init__(
        self,
        latitude: float,
        longitude: float,
        date: datetime.datetime,
        ephemeris: str = "de421.bsp",
    ) -> None:
        self.ts = load.timescale()
        self.planets = load(ephemeris)
        self.earth = self.planets["earth"]
        self.loaded_planets = {
            planet_name: self.planets[referential_name]
            for planet_name, referential_name in self.PLANETS_TO_LOAD.items()
        }
        self.latitude = latitude
        self.longitude = longitude
        self.location = self.earth + wgs84.latlon(latitude, longitude)
        self.date = date
        self.t = self.ts.from_datetime(self.date)

    def find_radec(
        self,
        planet_name: str,
        t: timelib.Time,
    ) -> tuple[units.Angle, units.Angle, units.Distance]:
        planet = self.loaded_planets[planet_name]
        astrometric = self.location.at(t).observe(planet)
        ra, dec, distance = astrometric.radec()
        return (ra, dec, distance)

    def altaz(
        self,
        planet_name: str,
        t: timelib.Time,
    ) -> Observation:
        planet = self.loaded_planets[planet_name]
        apparent = self.location.at(t).observe(planet).apparent()
        alt, az, dist = apparent.altaz()
        return Observation(
            planet_name.capitalize(),
            float(alt.degrees),
            float(az.degrees),
            float(dist.au),
            bool(alt.degrees > 0),
        )

    def observable_planets(self):
        planets = [self.altaz(planet, self.t) for planet in self.loaded_planets]
        return [planet for planet in planets if planet.visible]

    def rate_observable_planets(self):
        interest_bonus = {
            "Venus": 5,
            "Jupiter": 10,
            "Saturn": 15,
            "Mars": 8,
            "Uranus": 3,
            "Neptune": 1,
        }
        obserable_planets = self.observable_planets()
        for planet in obserable_planets:
            planet.rating = (
                int(planet.altitude_deg / 90 * 50)
                + max(0, 10 - self.VISUAL_MAGNITUDE[planet.planet_name])
                + interest_bonus[planet.planet_name]
            )

        return obserable_planets


if __name__ == "__main__":
    observer = Observer(
        42.42,
        23.20,
        datetime.datetime(2026, 2, 25, 21, 39, 00, 00, datetime.timezone.utc),
    )

    print(observer.observable_planets())
