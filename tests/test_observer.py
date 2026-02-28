from unittest import TestCase
import datetime
import unittest
from observer import Observer


class TestObserver(TestCase):
    def setUp(self) -> None:
        self.observer = Observer(
            42.42,
            23.20,
            datetime.datetime(2026, 2, 25, 21, 39, 00, 00, datetime.timezone.utc),
        )
        return super().setUp()

    def test_altaz_returns_altitude_in_bounds(self) -> None:
        altaz = self.observer.altaz("mars", self.observer.t)
        self.assertGreater(altaz.altitude_deg, -90)
        self.assertLessEqual(altaz.altitude_deg, 90)

    def test_visible_flag_is_false_if_altitude_less_than_90(self) -> None:
        altaz = self.observer.altaz("mars", self.observer.t)
        self.assertEqual(altaz.visible, altaz.altitude_deg > 0)


if __name__ == "__main__":
    unittest.main()
