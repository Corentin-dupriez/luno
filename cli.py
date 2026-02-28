import argparse
import datetime
from observer import Observer


def main() -> None:
    parser = argparse.ArgumentParser(
        description="A tool to visualise which planets are visible for observation from a certain place and date on earth"
    )
    parser.add_argument(
        "--latitude", type=float, help="The latitude of the point of observation"
    )
    parser.add_argument(
        "--longitude", type=float, help="The longitude of the point of observation"
    )

    args = parser.parse_args()

    observer = Observer(
        args.latitude,
        args.longitude,
        datetime.datetime(2026, 2, 25, 21, 39, 00, 00, datetime.timezone.utc),
    )
    print(observer)


if __name__ == "__main__":
    main()
