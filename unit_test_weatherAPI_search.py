from unittest import TestCase
from weatherAPI_search import get_weather_by_location_and_date


class TestGetWeatherByLocationFunction(TestCase):

    def test_date_valid_1_day(self):
        expected = [{'average_temp': 8.1, 'date': '2023-12-31'}]
        self.assertEqual(expected, get_weather_by_location_and_date("London", "2023-12-31", "2023-12-31"))

    def test_date_valid_2_days_different_year(self):
        expected = [{'average_temp': 8.1, 'date': '2023-12-31'}, {'average_temp': 8.3, 'date': '2024-01-01'}]
        self.assertEqual(expected, get_weather_by_location_and_date("London", "2023-12-31", "2024-01-01"))

    def test_date_valid_14_days(self):
        expected = [{'date': '2023-12-31', 'average_temp': 8.1}, {'date': '2024-01-01', 'average_temp': 8.3}, {'date': '2024-01-02', 'average_temp': 11.1}, {'date': '2024-01-03', 'average_temp': 10.1}, {'date': '2024-01-04', 'average_temp': 7.2}, {'date': '2024-01-05', 'average_temp': 5.5}, {'date': '2024-01-06', 'average_temp': 5.5}, {'date': '2024-01-07', 'average_temp': 3.4}, {'date': '2024-01-08', 'average_temp': 2.4}, {'date': '2024-01-09', 'average_temp': 2.1}, {'date': '2024-01-10', 'average_temp': 2.1}, {'date': '2024-01-11', 'average_temp': 3.1}, {'date': '2024-01-12', 'average_temp': 5.3}, {'date': '2024-01-13', 'average_temp': 3.1}]
        self.assertEqual(expected, get_weather_by_location_and_date("London", "2023-12-31", "2024-01-13"))

    def test_location_valid_Manchester(self):
        expected = [{'average_temp': 6.2, 'date': '2023-12-31'}]
        self.assertEqual(expected, get_weather_by_location_and_date("Manchester", "2023-12-31", "2023-12-31"))

    def test_date_invalid_0_days(self):
        expected = None
        self.assertEqual(expected, get_weather_by_location_and_date("Manchester", "", ""))

    def test_location_invalid_L_o_n_d_o_n(self):
        expected = None
        self.assertEqual(expected, get_weather_by_location_and_date("L-o-n-d-o-n", "2023-01-01", "2023-01-01"))

    def test_location_boundary_long_name(self):
        expected = None
        self.assertEqual(expected, get_weather_by_location_and_date("Maaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaanchester", "2023-01-01", "2023-01-01"))

    def test_date_boundary_very_old(self):
        expected = None
        self.assertEqual(expected, get_weather_by_location_and_date("London", "1000-01-01", "1000-01-01"))
