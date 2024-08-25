import unittest
from unittest.mock import patch, MagicMock
from get_hotels import (
    city_search, get_number_of_people, get_number_of_rooms, get_selected_filters,
    find_hotels, display_hotels_with_links, get_hotel_choice, get_cityID_for_city_in_country,
    save_hotel_to_favourite, get_hotels, CityNotFoundError
)


class TestGetHotels(unittest.TestCase):

    @patch('get_hotels.search_cities')
    def test_city_search_valid(self, mock_search_cities):
        mock_search_cities.return_value = {
            'results': {'locations': [{'cityName': 'London', 'id': 1}]}
        }
        result = city_search('London')
        self.assertEqual(result['cityName'], 'London')

    @patch('get_hotels.search_cities')
    def test_city_search_not_found(self, mock_search_cities):
        mock_search_cities.return_value = {'results': {'locations': []}}
        with self.assertRaises(CityNotFoundError):
            city_search('InvalidCity')

    @patch('builtins.input', side_effect=['2'])
    def test_get_number_of_people_valid(self, mock_input):
        self.assertEqual(get_number_of_people(), 2)

    @patch('builtins.input', side_effect=['5', '4'])
    def test_get_number_of_people_invalid(self, mock_input):
        # Checking if the function keeps prompting until a valid number is entered
        self.assertEqual(get_number_of_people(), 4)  # Checking that it finally returns the valid number

    @patch('builtins.input', side_effect=['2'])  # Expecting 2 rooms for 2 adults
    def test_get_number_of_rooms_valid(self, mock_input):
        result = get_number_of_rooms(2)
        self.assertEqual(result, 2)

    @patch('builtins.input', side_effect=['4', '3'])
    def test_get_number_of_rooms_invalid(self, mock_input):
        # Testing for 4 adults, initially enter 4 rooms which is too many, then correct to 3 rooms
        self.assertEqual(get_number_of_rooms(4), 3)

    @patch('builtins.input', side_effect=['1,2,3'])
    def test_get_selected_filters_valid(self, mock_input):
        self.assertEqual(get_selected_filters(), ['center', 'luxury', '3-stars'])

    @patch('builtins.input', side_effect=['99', '1'])
    def test_get_selected_filters_invalid(self, mock_input):
        self.assertEqual(get_selected_filters(), ['center'])

    @patch('get_hotels.fetch_hotels_with_filters')
    @patch('get_hotels.fetch_price')
    def test_find_hotels_valid(self, mock_fetch_price, mock_fetch_hotels_with_filters):
        mock_fetch_hotels_with_filters.return_value = [{'hotel_id': 1, 'name': 'Hotel One'}]
        mock_fetch_price.return_value = 100
        result = find_hotels(1, '2024-09-01', '2024-09-10', ['center'], 1, 2)
        self.assertEqual(result[0]['price'], 100)

    @patch('builtins.input', side_effect=['1'])
    def test_get_hotel_choice_valid(self, mock_input):
        hotel_prices = [{'hotelName': 'Hotel One', 'hotelId': 1, 'price': 100}]
        self.assertEqual(get_hotel_choice(hotel_prices)['hotelName'], 'Hotel One')

    @patch('get_hotels.Location.get_city_id')
    def test_get_cityID_for_city_in_country_valid(self, mock_get_city_id):
        mock_get_city_id.return_value = 123
        result = get_cityID_for_city_in_country('London', 'UK')
        self.assertEqual(result, '123')

    @patch('get_hotels.SavingToFavourites.save_favourite_hotels')
    def test_save_hotel_to_favourite(self, mock_save_favourite_hotels):
        mock_save_favourite_hotels.return_value = None
        results = {'hotelId': 1, 'hotelName': 'Hotel One'}
        save_hotel_to_favourite(results, 'London', '123', 'UK', 'uk')
        mock_save_favourite_hotels.assert_called_once()


if __name__ == '__main__':
    unittest.main()
