import unittest
from unittest.mock import MagicMock, patch
from get_location import Location
from database.db_utils import DbConnectionError


class TestLocation(unittest.TestCase):

    def setUp(self):
        """Setting up the Location object and mock the database connection."""
        self.mock_db = patch('get_location.Database').start()
        self.mock_db_instance = self.mock_db.return_value
        self.location = Location(host='mock_host', user='mock_user', password='mock_pass', db_name='mock_db')

    def tearDown(self):
        """Stopping the patch after each test."""
        patch.stopall()

    def test_get_countries_valid(self):
        """Testing fetching valid countries."""
        self.mock_db_instance.fetch_data.return_value = [('France',), ('Germany',), ('Spain',)]

        result = self.location.get_countries()
        self.assertEqual(result, ['France', 'Germany', 'Spain'])
        self.mock_db_instance.fetch_data.assert_called_once_with(table_name='countries', columns=['country_name'])

    def test_get_countries_no_results(self):
        """Testing fetching countries with no data."""
        self.mock_db_instance.fetch_data.return_value = []

        result = self.location.get_countries()
        self.assertEqual(result, [])
        self.mock_db_instance.fetch_data.assert_called_once_with(table_name='countries', columns=['country_name'])

    def test_get_countries_db_connection_error(self):
        """Testing fetching countries when a DbConnectionError occurs."""
        self.mock_db_instance.fetch_data.side_effect = DbConnectionError("DB Connection Failed")

        result = self.location.get_countries()
        self.assertIsNone(result)
        self.mock_db_instance.fetch_data.assert_called_once_with(table_name='countries', columns=['country_name'])

    def test_get_cities_by_country_valid(self):
        """Testing fetching cities by valid country."""
        self.mock_db_instance.fetch_data.return_value = [('Paris',), ('Lyon',), ('Marseille',)]

        with patch('builtins.input', side_effect=['1']):
            city_choice = self.location.get_cities_by_country('France')
            self.assertEqual(city_choice, 'paris')
            self.mock_db_instance.fetch_data.assert_called_once_with(
                table_name="cities",
                columns=['cities.city_name'],
                join="INNER JOIN countries ON cities.country_code = countries.country_code",
                conditions="countries.country_name = 'France'"
            )

    def test_get_cities_by_country_invalid(self):
        """Testing fetching cities with no cities for a given country."""
        self.mock_db_instance.fetch_data.return_value = []

        result = self.location.get_cities_by_country('InvalidCountry')
        self.assertIsNone(result)
        self.mock_db_instance.fetch_data.assert_called_once_with(
            table_name="cities",
            columns=['cities.city_name'],
            join="INNER JOIN countries ON cities.country_code = countries.country_code",
            conditions="countries.country_name = 'InvalidCountry'"
        )

    def test_get_holiday_type_cities_valid(self):
        """Testing fetching cities for valid holiday types."""
        self.mock_db_instance.fetch_data.return_value = [('Paris', 'France', 'museums'), ('Lyon', 'France', 'museums')]

        with patch('get_location.input_check.get_input', return_value='y'):
            # First input for selecting 'museums', second for selecting the city
            with patch('builtins.input', side_effect=['museums', '1']):
                chosen_city, _ = self.location.get_holiday_type_cities()
                self.mock_db_instance.fetch_data.assert_called_once_with(
                    table_name="cities",
                    columns=['cities.city_name', 'countries.country_name', 'cities.keyword'],
                    join="INNER JOIN countries ON cities.country_code = countries.country_code",
                    conditions="cities.keyword IN ('museums')"
                )
                self.assertEqual(chosen_city, 'Paris')

    def test_get_holiday_type_cities_multiple_valid(self):
        """Testing fetching cities for multiple valid holiday types."""
        self.mock_db_instance.fetch_data.return_value = [('Paris', 'France', 'museums'), ('Nice', 'France', 'beaches')]

        with patch('get_location.input_check.get_input', return_value='y'):
            # First input for selecting 'museums, beaches', second for selecting the city
            with patch('builtins.input', side_effect=['museums, beaches', '1']):
                chosen_city, _ = self.location.get_holiday_type_cities()
                self.mock_db_instance.fetch_data.assert_called_once_with(
                    table_name="cities",
                    columns=['cities.city_name', 'countries.country_name', 'cities.keyword'],
                    join="INNER JOIN countries ON cities.country_code = countries.country_code",
                    conditions="cities.keyword IN ('museums', 'beaches')"
                )
                self.assertEqual(chosen_city, 'Paris')

    def test_get_holiday_type_cities_invalid(self):
        """Testing fetching cities for an invalid holiday type and retry."""
        self.mock_db_instance.fetch_data.return_value = []

        with patch('builtins.input', side_effect=['invalid_type', 'museums']):
            self.location.get_holiday_type_cities()
            self.mock_db_instance.fetch_data.assert_called_once_with(
                table_name="cities",
                columns=['cities.city_name', 'countries.country_name', 'cities.keyword'],
                join="INNER JOIN countries ON cities.country_code = countries.country_code",
                conditions="cities.keyword IN ('museums')"
            )

    def test_get_holiday_type_countries_valid(self):
        """Testing fetching countries for a valid holiday type."""
        self.mock_db_instance.fetch_data.return_value = [('France',), ('Italy',)]

        with patch('builtins.input', return_value='wine'):
            self.location.get_holiday_type_countries()
            self.mock_db_instance.fetch_data.assert_called_once_with(
                table_name="countries",
                columns=['DISTINCT countries.country_name'],
                join="INNER JOIN cities ON countries.country_code = cities.country_code",
                conditions="cities.keyword IN (wine)"
            )

    def test_get_holiday_type_countries_multiple_valid(self):
        """Testing fetching countries for multiple valid holiday types."""
        self.mock_db_instance.fetch_data.return_value = [('France',), ('Italy',)]

        with patch('builtins.input', return_value='wine, fashion'):
            self.location.get_holiday_type_countries()
            self.mock_db_instance.fetch_data.assert_called_once_with(
                table_name="countries",
                columns=['DISTINCT countries.country_name'],
                join="INNER JOIN cities ON countries.country_code = cities.country_code",
                conditions="cities.keyword IN ('wine', 'fashion')"
            )

    def test_get_holiday_type_countries_invalid(self):
        """Testing fetching countries for an invalid holiday type and retry."""
        self.mock_db_instance.fetch_data.return_value = []

        with patch('builtins.input', side_effect=['invalid_type', 'wine']):
            self.location.get_holiday_type_countries()
            self.mock_db_instance.fetch_data.assert_called_once_with(
                table_name="countries",
                columns=['DISTINCT countries.country_name'],
                join="INNER JOIN cities ON countries.country_code = cities.country_code",
                conditions="cities.keyword IN ('wine')"
            )

    def test_get_cities_by_country_invalid_number(self):
        """Test get_cities_by_country when an invalid number is entered."""
        self.mock_db_instance.fetch_data.return_value = [('Paris',), ('Lyon',), ('Marseille',)]

        with patch('builtins.input', side_effect=['10', '2']):
            city_choice = self.location.get_cities_by_country('France')
            self.assertEqual(city_choice, 'lyon')

    def test_get_holiday_type_cities_empty_input(self):
        """Test get_holiday_type_cities when no holiday type is provided."""
        with patch('builtins.input', side_effect=['', 'museums']):
            self.location.get_holiday_type_cities()
            self.mock_db_instance.fetch_data.assert_called_once_with(
                table_name="cities",
                columns=['cities.city_name', 'countries.country_name', 'cities.keyword'],
                join="INNER JOIN countries ON cities.country_code = countries.country_code",
                conditions="cities.keyword IN ('museums')"
            )

    def test_close(self):
        """Test closing the database connection."""
        self.location.close()
        self.mock_db_instance.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
