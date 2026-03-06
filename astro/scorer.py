from astro.observer import Observation


class ObservationScorer:
    VISUAL_MAGNITUDE = {
        "Venus": -4,
        "Jupiter": -2.2,
        "Mercury": -2.5,
        "Mars": -2.9,
        "Saturn": -0.5,
        "Uranus": 5.7,
        "Neptune": 7.8,
    }

    # TODO: Implement other inputs than observation
    def score(
        self, observation: Observation, moon=None, weather=None, sun_alt=None
    ) -> int:
        score = 0
        score += int((observation.altitude_deg / 90) * 50)
        score += max(0, 10 + self.VISUAL_MAGNITUDE[observation.planet_name])
        return score
