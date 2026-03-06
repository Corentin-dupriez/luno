from unittest.mock import patch, Mock
from geo.geocoder import city_geoposition
from unittest import TestCase


class TestObserver(TestCase):
    @patch("geo.geocoder.requests.get")
    def test_city_geoposition_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [{"lat": "42.6977", "lon": "23.3219"}]
        mock_get.return_value = mock_response
        result = city_geoposition("Sofia")
        assert result == (42.6977, 23.3219)

    @patch("geo.geocoder.requests.get")
    def test_city_geoposition_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = []

        mock_get.return_value = mock_response

        result = city_geoposition("UnknownCity")

        assert result is None
