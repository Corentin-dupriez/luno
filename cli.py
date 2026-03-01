import argparse
import datetime
import geocoder
from observer import Observer


class ArgumentMissing(Exception):
    pass


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
        latitude, longitude = geocoder.city_geoposition(args.city)
    elif args.latitude and args.longitude and not args.city:
        latitude, longitude = args.latitude, args.longitude
    else:
        raise ArgumentMissing(
            "You should enter the city name OR latitude and longitude"
        )

    observer = Observer(
        latitude,
        longitude,
        datetime.datetime(2026, 2, 25, 21, 39, 00, 00, datetime.timezone.utc),
    )
    print(observer)


if __name__ == "__main__":
    main()
