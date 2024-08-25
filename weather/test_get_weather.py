import unittest
from weather import get_weather
from datetime import date, datetime


class TestFindWeatherFunction(unittest.TestCase):
    def test_weather_history_endpoint_valid(self):
        self.input_weather_data_location = "London"
        self.input_weather_data_start_date = datetime.strptime('2024-05-01', "%Y-%m-%d").date()
        self.input_weather_data_end_date = datetime.strptime('2024-05-10', "%Y-%m-%d").date()
        self.expect = [{'average_temp': 12.9, 'date': '2024-05-01'},
                       {'average_temp': 11.6, 'date': '2024-05-02'},
                       {'average_temp': 10.0, 'date': '2024-05-03'},
                       {'average_temp': 11.8, 'date': '2024-05-04'},
                       {'average_temp': 12.6, 'date': '2024-05-05'},
                       {'average_temp': 12.2, 'date': '2024-05-06'},
                       {'average_temp': 14.3, 'date': '2024-05-07'},
                       {'average_temp': 14.8, 'date': '2024-05-08'},
                       {'average_temp': 15.7, 'date': '2024-05-09'},
                       {'average_temp': 15.8, 'date': '2024-05-10'}]
        self.assertEqual(self.expect, get_weather.find_weather(self.input_weather_data_location,
                                                                       self.input_weather_data_start_date,
                                                                       self.input_weather_data_end_date))

    def test_weather_future_endpoint_valid(self):
        self.input_weather_data_location = "London"
        self.input_weather_data_start_date = datetime.strptime('2024-10-01', "%Y-%m-%d").date()
        self.input_weather_data_end_date = datetime.strptime('2024-10-03', "%Y-%m-%d").date()
        self.expect = [{'average_temp': 14.5, 'date': '2024-10-01'}, {'average_temp': 13.9, 'date': '2024-10-02'},
                       {'average_temp': 13.9, 'date': '2024-10-03'}]
        self.assertEqual(self.expect, get_weather.find_weather(self.input_weather_data_location,
                                                                       self.input_weather_data_start_date,
                                                                       self.input_weather_data_end_date))


class TestAddDaysFunction(unittest.TestCase):

    def test_add_days_valid_1(self):
        self.number_to_add = 1
        self.date_to_add_days_to = date(2024, 8, 21)
        self.expected = '2024-08-22'
        self.assertEqual(self.expected, str(get_weather.add_days(self.number_to_add, self.date_to_add_days_to)))


class TestSubtractDaysFunction(unittest.TestCase):

    def test_subtract_days_valid_1(self):
        self.number_to_subtract = 1
        self.date_to_subtract_from = date(2024, 8, 21)
        self.expected = '2024-08-20'
        self.assertEqual(self.expected, str(get_weather.subtract_days
                                            (self.number_to_subtract, self.date_to_subtract_from)))


class TestWeatherApiEndpointCalculatorFunction(unittest.TestCase):

    def test_calculator_valid_history_2024_05_01(self):
        self.past_date = datetime.strptime('2024-05-01', "%Y-%m-%d").date()
        self.expected = 'history'
        self.assertEqual(self.expected, get_weather.weather_api_endpoint_calculator(self.past_date))

    def test_calculator_valid_future_2024_12_01(self):
        self.future_date = datetime.strptime('2024-12-01', "%Y-%m-%d").date()
        self.expected = 'future'
        self.assertEqual(self.expected, get_weather.weather_api_endpoint_calculator(self.future_date))

    def test_calculator_valid_300_or_more_days_in_the_future_2025_06_01(self):
        self.future_date = datetime.strptime('2025-07-01', "%Y-%m-%d").date()
        self.expected = 'history'
        self.assertEqual(self.expected, get_weather.weather_api_endpoint_calculator(self.future_date))

    def test_calculator_14_days_after_rule_invalid_13_days(self):
        present_date = datetime.today().date()
        self.number_to_add = get_weather.add_days(13, present_date)
        self.expected = None
        self.assertEqual(self.expected, get_weather.weather_api_endpoint_calculator(self.number_to_add))

    def test_calculator_14_days_after_rule_valid_15_days(self):
        present_date = datetime.today().date()
        self.number_to_add = get_weather.add_days(15, present_date)
        self.expected = 'future'
        self.assertEqual(self.expected, get_weather.weather_api_endpoint_calculator(self.number_to_add))

    def test_calculator_14_days_after_rule_boundary_14_days(self):
        present_date = datetime.today().date()
        self.number_to_add = get_weather.add_days(14, present_date)
        self.expected = 'future'
        self.assertEqual(self.expected, get_weather.weather_api_endpoint_calculator(self.number_to_add))

    def test_calculator_14_days_before_rule_valid_12_days(self):
        present_date = datetime.today().date()
        self.number_to_subtract = get_weather.subtract_days(12, present_date)
        self.expected = None
        self.assertEqual(self.expected, get_weather.weather_api_endpoint_calculator(self.number_to_subtract))

    def test_calculator_14_days_before_rule_invalid_15_days(self):
        present_date = datetime.today().date()
        self.number_to_subtract = get_weather.subtract_days(15, present_date)
        self.expected = 'history'
        self.assertEqual(self.expected, get_weather.weather_api_endpoint_calculator(self.number_to_subtract))

    def test_calculator_14_days_before_rule_boundary_14_days(self):
        present_date = datetime.today().date()
        self.number_to_subtract = get_weather.subtract_days(14, present_date)
        self.expected = None
        self.assertEqual(self.expected,get_weather.weather_api_endpoint_calculator(self.number_to_subtract))

    def test_calculator_14_days_before_rule_boundary_0_days(self):
        present_date = datetime.today().date()
        self.number_to_subtract = get_weather.subtract_days(0, present_date)
        self.expected = None
        self.assertEqual(self.expected, get_weather.weather_api_endpoint_calculator(self.number_to_subtract))


class TestGetMinMaxAvgTempFunction(unittest.TestCase):

    def test_get_min_max_avg_valid_london_14_5_4_5_5_5_history(self):
        self.city = 'London'
        self.list_for_max_val = [{'average_temp': 14.5, 'date': '2024-10-01'},
                                 {'average_temp': 4.5, 'date': '2024-10-02'},
                                 {'average_temp': 5.5, 'date': '2024-10-03'}]
        self.endpoint = 'history'
        self.expected = ('The weather last year on the same dates in London was an average of 8.2°C, '
                         'with the lowest being 4.5°C and the highest being 14.5°C.')
        self.assertEqual(self.expected,
                        get_weather.get_minimum_maximum_average_temperature(self.city, self.list_for_max_val,
                                                                                     self.endpoint))

    def test_get_min_max_avg_valid_london_14_5_4_5_5_5future(self):
        self.city = 'London'
        self.list_for_max_val = [{'average_temp': 14.5, 'date': '2024-10-01'},
                                 {'average_temp': 4.5, 'date': '2024-10-02'},
                                 {'average_temp': 5.5, 'date': '2024-10-03'}]
        self.endpoint = 'future'
        self.expected = ('The predicted weather for London on the selected dates will be an average of 8.2°C, '
                         'with the lowest being 4.5°C and the highest being 14.5°C.')
        self.assertEqual(self.expected,
                        get_weather.get_minimum_maximum_average_temperature(self.city, self.list_for_max_val,
                                                                                     self.endpoint))


class TestFindMinValFromDictFunction(unittest.TestCase):

    def test_find_min_val_from_dict(self):
        self.list_for_min_val = [{'average_temp': 14.5, 'date': '2024-10-01'},
                                 {'average_temp': 4.5, 'date': '2024-10-02'},
                                 {'average_temp': 5.5, 'date': '2024-10-03'}]
        self.expected = 4.5
        self.assertEqual(self.expected, get_weather.find_min_val_from_dict(self.list_for_min_val))


class TestFindMaxValFromDictFunction(unittest.TestCase):

    def test_find_max_val_from_dict(self):
        self.list_for_max_val = [{'average_temp': 14.5, 'date': '2024-10-01'},
                                 {'average_temp': 4.5, 'date': '2024-10-02'},
                                 {'average_temp': 5.5, 'date': '2024-10-03'}]
        self.expected = 14.5
        self.assertEqual(self.expected,get_weather.find_max_val_from_dict(self.list_for_max_val))


class TestFindAverageFromDictFunction(unittest.TestCase):

    def test_find_avg_temp_from_dict(self):
        self.list_for_avg_val = [{'average_temp': 14.5, 'date': '2024-10-01'},
                                 {'average_temp': 4.5, 'date': '2024-10-02'},
                                 {'average_temp': 5.5, 'date': '2024-10-03'}]
        self.expected = 8.2
        self.assertEqual(self.expected, get_weather.find_avg_val_from_dict(self.list_for_avg_val))


class TestReturnAverageFunction(unittest.TestCase):

    def test_find_avg_temp_from_dict(self):
        self.values_for_average_calc = [14.5, 4.5, 5.5]
        self.expected = 8.2
        self.assertEqual(self.expected,get_weather.return_average_number(self.values_for_average_calc))


if __name__ == "__main__":
    unittest.main(verbosity=1)
