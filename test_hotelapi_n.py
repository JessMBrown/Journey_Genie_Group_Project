import requests
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from hotelapi_n import(
    search_cities,
    fetch_hotels_with_filters,
    fetch_price,
    fetch_hotel_details_with_links
)


class TestHotelAPI(unittest.TestCase):

    @patch('hotelapi_n.requests.get')
    def test_search_cities_valid(self, mock_get):
        # Mocking a successful response with sample data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [
                {'name': 'City1', 'locationId': 1},
                {'name': 'City2', 'locationId': 2}
            ]
        }
        mock_get.return_value = mock_response

        result = search_cities("London")
        self.assertEqual(len(result['results']), 2)
        self.assertEqual(result['results'][0]['name'], 'City1')

    @patch('hotelapi_n.requests.get')
    def test_search_cities_invalid(self, mock_get):
        # Mocking a failed response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = search_cities("InvalidCity")
        self.assertIsNone(result)

    @patch('hotelapi_n.requests.get')
    def test_search_cities_no_results(self, mock_get):
        # Mocking a successful response with no results
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': []}
        mock_get.return_value = mock_response

        result = search_cities("NoResultsCity")
        self.assertEqual(result['results'], [])

    @patch('hotelapi_n.requests.get')
    def test_fetch_hotels_with_filters_valid(self, mock_get):
        # Mocking a successful hotel search response with different filters
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Assuming we have two filters, 'luxury' and 'budget'
        mock_response.json.side_effect = [
            {'luxury': [{'name': 'Hotel1', 'id': 101}, {'name': 'Hotel2', 'id': 102}]},
            {'budget': [{'name': 'Hotel1', 'id': 101}, {'name': 'Hotel3', 'id': 103}]}
        ]
        mock_get.return_value = mock_response

        check_in = datetime(2024, 8, 15)
        check_out = datetime(2024, 8, 20)
        selected_filters = ['luxury', 'budget']
        result = fetch_hotels_with_filters(1, check_in, check_out, selected_filters)

        # Only Hotel1 should be returned since it matches both filters
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Hotel1')

    @patch('hotelapi_n.checking_api_response_success', return_value={})
    @patch('hotelapi_n.requests.get')
    def test_fetch_hotels_with_filters_invalid(self, mock_get, mock_check_response):
        # Mocking a failed response (500) and an empty dictionary return from the response handler
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        check_in = datetime(2024, 8, 15)
        check_out = datetime(2024, 8, 20)
        selected_filters = ['luxury', 'budget']
        result = fetch_hotels_with_filters(1, check_in, check_out, selected_filters)

        # Expecting an empty list because the mocked response is an empty dictionary
        self.assertEqual(result, [])

    @patch('hotelapi_n.requests.get')
    def test_fetch_price_valid(self, mock_get):
        # Mocking a successful price fetch response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'priceAvg': 150
        }
        mock_get.return_value = mock_response

        check_in = datetime(2024, 8, 15)
        check_out = datetime(2024, 8, 20)
        result = fetch_price(hotel_id=101, check_in=check_in, check_out=check_out, rooms=1, adults=2)
        self.assertEqual(result, 150)

    @patch('hotelapi_n.requests.get')
    def test_fetch_price_invalid(self, mock_get):
        # Mocking a failed price fetch response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        check_in = datetime(2024, 8, 15)
        check_out = datetime(2024, 8, 20)
        result = fetch_price(hotel_id=999, check_in=check_in, check_out=check_out, rooms=1, adults=2)
        self.assertEqual(result, "Price unavailable")

    @patch('hotelapi_n.requests.get')
    def test_fetch_price_no_price(self, mock_get):
        # Mocking a successful response with no price data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        check_in = datetime(2024, 8, 15)
        check_out = datetime(2024, 8, 20)
        result = fetch_price(hotel_id=101, check_in=check_in, check_out=check_out, rooms=1, adults=2)
        self.assertEqual(result, "Price unavailable")

    @patch('hotelapi_n.requests.get')
    def test_fetch_price_exception_handling(self, mock_get):
        # Mocking an exception during the API call
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        check_in = datetime(2024, 8, 15)
        check_out = datetime(2024, 8, 20)
        result = fetch_price(hotel_id=101, check_in=check_in, check_out=check_out)

        self.assertEqual(result, "Price unavailable")

    @patch('hotelapi_n.requests.get')
    def test_search_cities_empty_query(self, mock_get):
        # Mocking a successful response with no results
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'ok', 'results': {'locations': []}}
        mock_get.return_value = mock_response

        result = search_cities("")

        # Since the query is empty, we expect the results to be empty.
        self.assertEqual(result['results']['locations'], [])

    @patch('hotelapi_n.requests.get')
    def test_fetch_hotel_details_with_links_valid(self, mock_get):
        # Mocking a successful response with hotel data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'hotels': [
                {'id': 1, 'cityId': 101, 'name': {'en': 'Hotel One'}},
                {'id': 2, 'cityId': 102, 'name': {'en': 'Hotel Two'}}
            ]
        }
        mock_get.return_value = mock_response

        check_in = datetime(2024, 8, 15)
        check_out = datetime(2024, 8, 20)
        result = fetch_hotel_details_with_links(1, check_in, check_out)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['hotelName'], 'Hotel One')
        self.assertIn('Hotel+One', result[0]['link'])
        self.assertIn('hotelId=1', result[0]['link'])

    @patch('hotelapi_n.requests.get')
    def test_fetch_hotel_details_with_links_invalid(self, mock_get):
        # Mocking a failed response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        check_in = datetime(2024, 8, 15)
        check_out = datetime(2024, 8, 20)
        result = fetch_hotel_details_with_links(1, check_in, check_out)

        self.assertEqual(result, [])

    @patch('hotelapi_n.requests.get')
    def test_fetch_hotel_details_with_links_no_hotels(self, mock_get):
        # Mocking a successful response with no hotels
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'hotels': []}
        mock_get.return_value = mock_response

        check_in = datetime(2024, 8, 15)
        check_out = datetime(2024, 8, 20)
        result = fetch_hotel_details_with_links(1, check_in, check_out)

        self.assertEqual(result, [])

    @patch('hotelapi_n.requests.get')
    def test_fetch_hotel_details_with_links_no_hotel_key(self, mock_get):
        # Mocking a successful response with missing 'hotels' key
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        check_in = datetime(2024, 8, 15)
        check_out = datetime(2024, 8, 20)
        result = fetch_hotel_details_with_links(1, check_in, check_out)

        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
