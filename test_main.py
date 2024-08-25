import unittest
from unittest.mock import patch
from main import knows_destination, tailored_trip, take_me_anywhere, fetch_and_display_summary, plan_trip_details
from datetime import datetime
from location.get_location import Location
from config import HOST, PASSWORD, USER

planner = Location(host=HOST, user=USER, password=PASSWORD, db_name='destinations')


class TestKnowsDestination(unittest.TestCase):

    @patch('main.knows_destination')
    def test_knows_destination_valid(self, mock_of_knows_dest):
        mock_of_knows_dest.return_value = 'Spain'
        start_date = datetime.strptime('2024-05-01', "%Y-%m-%d").date()
        end_date = datetime.strptime('2024-05-02', "%Y-%m-%d").date()
        result = knows_destination(planner, start_date, end_date)
        self.assertEqual(result, 'Spain')


class TestTailoredTrip(unittest.TestCase):

    @patch('main.knows_destination')
    def test_tailored_trip(self, mock_of_tailored_trip):
        mock_of_tailored_trip.return_value = 'Spain'
        start_date = datetime.strptime('2024-05-01', "%Y-%m-%d").date()
        end_date = datetime.strptime('2024-05-02', "%Y-%m-%d").date()
        result = tailored_trip(planner, start_date, end_date)
        self.assertEqual(result, 'Spain')


class TestTakeMeAnywhere(unittest.TestCase):

    @patch('main.take_me_anywhere')
    def test_take_me_anywhere(self, mock_of_take_me_anywhere):
        mock_of_take_me_anywhere.return_value = 'Spain'
        start_date = datetime.strptime('2024-05-01', "%Y-%m-%d").date()
        end_date = datetime.strptime('2024-05-02', "%Y-%m-%d").date()
        result = take_me_anywhere(planner, start_date, end_date)
        self.assertEqual(result, 'Spain')


class TestFetchAndDisplaySummary(unittest.TestCase):

    @patch('main.fetch_and_display_summary')
    def test_fetch_and_display_summary(self, mock_of_fetch_and_display_summary):
        mock_of_fetch_and_display_summary.return_value = 'Spain'
        start_date = datetime.strptime('2024-05-01', "%Y-%m-%d").date()
        end_date = datetime.strptime('2024-05-02', "%Y-%m-%d").date()
        result = fetch_and_display_summary(start_date, end_date, saved_hotels, saved_activities, city_choice, chosen_country)
        self.assertEqual(result, 'Spain')


class TestPlanTripDetails(unittest.TestCase):

    @patch('main.plan_trip_details')
    def test_plan_trip_details(self, mock_of_plan_trip_details):
        mock_of_plan_trip_details.return_value = 'Spain'
        start_date = datetime.strptime('2024-05-01', "%Y-%m-%d").date()
        end_date = datetime.strptime('2024-05-02', "%Y-%m-%d").date()
        result = plan_trip_details(city_choice, start_date, end_date, chosen_country)
        self.assertEqual(result, 'Spain')

if __name__ == "__main__":
    unittest.main(verbosity=1)
