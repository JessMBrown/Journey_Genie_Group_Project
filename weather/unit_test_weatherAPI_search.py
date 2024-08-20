import unittest
from weather_api_search import GetWeatherByLocation


class TestGetWeatherByLocationFunction(unittest.TestCase):

    def test_date_valid_1_day(self):
        # create a variable to pass to the class GetWeatherByLocation with valid details
        self.input_data = GetWeatherByLocation("London", "2023-12-31", "2023-12-31")
        # define the expected response
        self.expected = [{'average_temp': 8.1, 'date': '2023-12-31'}]
        # compare the expected response with the response received from the get_historic_weather_by_location_and_date
        # function using the inherited data from the class GetWeatherByLocation
        self.assertEqual(self.expected, GetWeatherByLocation.get_historic_weather_by_location_and_date(self.input_data))

    def test_date_valid_2_days_different_year(self):
        self.input_data = GetWeatherByLocation("London", "2023-12-31", "2024-01-01")
        self.expected = [{'average_temp': 8.1, 'date': '2023-12-31'}, {'average_temp': 8.3, 'date': '2024-01-01'}]
        self.assertEqual(self.expected, GetWeatherByLocation.get_historic_weather_by_location_and_date(self.input_data))

    def test_date_valid_14_days(self):
        self.input_data = GetWeatherByLocation("London", "2023-12-31", "2024-01-13")
        self.expected = [{'date': '2023-12-31', 'average_temp': 8.1}, {'date': '2024-01-01', 'average_temp': 8.3},
                         {'date': '2024-01-02', 'average_temp': 11.1}, {'date': '2024-01-03', 'average_temp': 10.1},
                         {'date': '2024-01-04', 'average_temp': 7.2}, {'date': '2024-01-05', 'average_temp': 5.5},
                         {'date': '2024-01-06', 'average_temp': 5.5}, {'date': '2024-01-07', 'average_temp': 3.4},
                         {'date': '2024-01-08', 'average_temp': 2.4}, {'date': '2024-01-09', 'average_temp': 2.1},
                         {'date': '2024-01-10', 'average_temp': 2.1}, {'date': '2024-01-11', 'average_temp': 3.1},
                         {'date': '2024-01-12', 'average_temp': 5.3}, {'date': '2024-01-13', 'average_temp': 3.1}]
        self.assertEqual(self.expected, GetWeatherByLocation.get_historic_weather_by_location_and_date(self.input_data))

    def test_location_valid_Manchester(self):
        self.input_data = GetWeatherByLocation("Manchester", "2023-12-31", "2023-12-31")
        self.expected = [{'average_temp': 6.2, 'date': '2023-12-31'}]
        self.assertEqual(self.expected, GetWeatherByLocation.get_historic_weather_by_location_and_date(self.input_data))

    def test_date_invalid_0_days(self):
        self.input_data = GetWeatherByLocation("Manchester", "", "")
        self.expected = None
        self.assertEqual(self.expected, GetWeatherByLocation.get_historic_weather_by_location_and_date(self.input_data))

    def test_location_invalid_L_o_n_d_o_n(self):
        self.input_data = GetWeatherByLocation("L-o-n-d-o-n", "2023-01-01", "2023-01-01")
        self.expected = None
        self.assertEqual(self.expected, GetWeatherByLocation.get_historic_weather_by_location_and_date(self.input_data))

    def test_location_boundary_long_name(self):
        self.input_data = GetWeatherByLocation(
            "Maaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaanchester", "2023-01-01",
            "2023-01-01")
        self.expected = None
        self.assertEqual(self.expected, GetWeatherByLocation.get_historic_weather_by_location_and_date(
            self.input_data))

    def test_date_boundary_very_old(self):
        self.input_data = GetWeatherByLocation("London", "1000-01-01", "1000-01-01")
        self.expected = None
        self.assertEqual(self.expected, GetWeatherByLocation.get_historic_weather_by_location_and_date(self.input_data))


# add runner to enable automation of running tests using the 'python3 unit_test_weatherAPI_search.py' command
if __name__ == "__main__":
    unittest.main(verbosity=1)
