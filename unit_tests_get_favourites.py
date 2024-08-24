import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from get_favourites import SavingToFavourites


class TestSavingToFavourites(unittest.TestCase):

    @patch('get_favourites.SavingToFavourites.store_favourites_in_database')
    @patch('get_favourites.UserInputCheck')
    def test_save_favourite_hotels_yes(self, mock_input_check, mock_store_favourites):
        # Mocking the user input to save the hotel
        mock_input_check.get_input.return_value = 'y'
        fav_manager = SavingToFavourites()

        # Save a favourite hotel
        fav_manager.save_favourite_hotels(
            hotel_id=101,
            hotel_name="Luxury Hotel",
            city_choice="Paris",
            city_id=1,
            input_check=mock_input_check,
            chosen_country="France",
            country_code="FR"
        )

        # Check if the hotel is added to favourite_hotels
        self.assertEqual(len(fav_manager.favourite_hotels), 1)
        self.assertEqual(fav_manager.favourite_hotels[0]['name'], "Luxury Hotel")

        # Verify if the database storage function is called
        mock_store_favourites.assert_called_once()

    @patch('get_favourites.SavingToFavourites.store_favourites_in_database')
    @patch('get_favourites.UserInputCheck')
    def test_save_favourite_activities_yes(self, mock_input_check, mock_store_favourites):
        # Mocking the user input to save the activity
        mock_input_check.get_input.return_value = 'y'
        fav_manager = SavingToFavourites()

        # Save a favourite activity
        fav_manager.save_favourite_activities(
            xid="activity_001",
            activity_name="Museum Visit",
            city_choice="London",
            city_id=2,
            input_check=mock_input_check,
            chosen_country="UK",
            country_code="GB"
        )

        # Check if the activity is added to favourite_activities
        self.assertEqual(len(fav_manager.favourite_activities), 1)
        self.assertEqual(fav_manager.favourite_activities[0]['name'], "Museum Visit")

        # Verify if the database storage function is called
        mock_store_favourites.assert_called_once()

    @patch('get_favourites.UserInputCheck')
    def test_save_favourite_hotels_no(self, mock_input_check):
        # Mocking the user input to not save the hotel
        mock_input_check.get_input.return_value = 'n'
        fav_manager = SavingToFavourites()

        # Save a favourite hotel
        fav_manager.save_favourite_hotels(
            hotel_id=102,
            hotel_name="Budget Hotel",
            city_choice="Berlin",
            city_id=3,
            input_check=mock_input_check,
            chosen_country="Germany",
            country_code="DE"
        )

        # Check that no hotels are added to the list
        self.assertEqual(len(fav_manager.favourite_hotels), 0)

    @patch('get_favourites.UserInputCheck')
    def test_save_favourite_activities_no(self, mock_input_check):
        # Mocking the user input to not save the activity
        mock_input_check.get_input.return_value = 'n'
        fav_manager = SavingToFavourites()

        # Save a favourite activity
        fav_manager.save_favourite_activities(
            xid="activity_002",
            activity_name="City Tour",
            city_choice="Rome",
            city_id=4,
            input_check=mock_input_check,
            chosen_country="Italy",
            country_code="IT"
        )

        # Check that no activities are added to the list
        self.assertEqual(len(fav_manager.favourite_activities), 0)

    @patch('get_favourites.SavingToFavourites.store_favourites_in_database')
    @patch('get_favourites.UserInputCheck')
    def test_save_favourites_database_failure(self, mock_input_check, mock_store_favourites):
        # Mocking the user input to save the hotel
        mock_input_check.get_input.return_value = 'y'
        # Mocking an exception in the database storage function
        mock_store_favourites.side_effect = Exception("Database Error")

        fav_manager = SavingToFavourites()

        # Save a favourite hotel
        fav_manager.save_favourite_hotels(
            hotel_id=103,
            hotel_name="Beach Resort",
            city_choice="Maldives",
            city_id=5,
            input_check=mock_input_check,
            chosen_country="Maldives",
            country_code="MV"
        )

        # Check if the hotel is added to favourite_hotels despite the database error
        self.assertEqual(len(fav_manager.favourite_hotels), 1)
        self.assertEqual(fav_manager.favourite_hotels[0]['name'], "Beach Resort")

        # Verify the database storage was attempted
        mock_store_favourites.assert_called_once()

    @patch('get_favourites.SavingToFavourites.store_favourites_in_database')
    @patch('get_favourites.UserInputCheck')
    def test_save_favourites_data_structure(self, mock_input_check, mock_store_favourites):
        # Mocking the user input to save the activity
        mock_input_check.get_input.return_value = 'y'
        fav_manager = SavingToFavourites()

        # Save a favourite activity
        fav_manager.save_favourite_activities(
            xid="activity_003",
            activity_name="Snorkeling",
            city_choice="Sydney",
            city_id=6,
            input_check=mock_input_check,
            chosen_country="Australia",
            country_code="AU"
        )

        # Check the structure of the saved activity
        saved_activity = fav_manager.favourite_activities[0]
        self.assertEqual(saved_activity['activitie id'], "activity_003")
        self.assertEqual(saved_activity['name'], "Snorkeling")
        self.assertEqual(saved_activity['city'], "Sydney")
        self.assertEqual(saved_activity['city_ID'], 6)
        self.assertEqual(saved_activity['country'], "Australia")
        self.assertEqual(saved_activity['country_code'], "AU")
        self.assertTrue('added_on' in saved_activity)


if __name__ == '__main__':
    unittest.main()
