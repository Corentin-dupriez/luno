import argparse
import datetime
from typing import List
import geo.geocoder as geocoder
from astro.observer import Observation, Observer
from astro.scorer import ObservationScorer


class ArgumentMissing(Exception):
    pass


class UnknownCity(Exception):
    pass


def display_visible_planets(planets: List[Observation]) -> None:
    ordered_planets = sorted(planets, key=lambda x: -x.scorer)
    print("Visible planets:")
    print(
        "\n".join(
            [f" - {planet.planet_name}, score: {planet.scorer}" for planet in planets]
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="A tool to visualise which planets are visible for observation from a certain place and date on earth"
    )
    parser.add_argument(
        "--latitude",
        "-lat",
        type=float,
        required=False,
        help="The latitude of the point of observation",
    )
    parser.add_argument(
        "--longitude",
        "-lon",
        type=float,
        required=False,
        help="The longitude of the point of observation",
    )

    parser.add_argument(
        "--city",
        "-c",
        type=str,
        required=False,
        help="The name of the city of observation",
    )

    args = parser.parse_args()

    if args.city and not args.latitude and not args.longitude:
        geoposition = geocoder.city_geoposition(args.city)
        if geoposition is None:
            raise UnknownCity("City not found")
        else:
            latitude, longitude = geoposition[0], geoposition[1]

    elif args.latitude and args.longitude and not args.city:
        latitude, longitude = args.latitude, args.longitude

    else:
        raise ArgumentMissing(
            "You should enter the city name OR latitude and longitude"
        )

    observer = Observer(
        latitude,
        longitude,
        datetime.datetime.now(),
    )
    planets = observer.observable_planets()
    for planet in planets:
        planet.scorer = ObservationScorer().score(planet)
    display_visible_planets(planets)


if __name__ == "__main__":
    main()
