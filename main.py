from skyfield.api import load, N, W, wgs84


def find_radec(
    latitude: float,
    longitude: float,
    planet: skyfield.vectorlib.VectorSum,
    t: skyfield.timelib.Time,
) -> list[skyfield.units.Angle, skyfield.units.Angle, skyfield.units.Distance]:
    city = earth + wgs84.latlon(latitude * N, longitude * W)
    astrometric = city.at(t).observe(planet)
    ra, dec, distance = astrometric.radec()
    return [ra, dec, distance]


ts = load.timescale()
t = ts.now()

planets = load("de421.bsp")

earth, mars = planets["earth"], planets["mars"]

print(find_radec(42.42, 23.20, mars, t))
