import unittest
from unittest.mock import patch, MagicMock
from get_mail import get_email, validate_email, store_email_in_database
from database.db_utils_oli import Database, DbConnectionError


class TestEmailFunctions(unittest.TestCase):

    @patch('builtins.input', side_effect=['y', 'John', 'john@example.com'])
    @patch('get_mail.store_email_in_database')  # Mocking the database storage function
    def test_get_email_valid_input(self, mock_store_email, mock_input):
        """Testing the get_email function with valid inputs."""
        get_email()

        # Checking that store_email_in_database was called with correct data
        mock_store_email.assert_called_once_with({
            'first_name': 'John',
            'email_address': 'john@example.com'
        })

    @patch('builtins.input', side_effect=['maybe', 'y', '123', 'John', 'no-at-symbol.com', 'john@example.com'])
    @patch('get_mail.store_email_in_database')
    def test_get_email_invalid_then_valid_input(self, mock_store_email, mock_input):
        """Testing get_email function with invalid inputs followed by valid ones."""
        get_email()

        # The database function should only be called once the input is valid
        mock_store_email.assert_called_once_with({
            'first_name': 'John',
            'email_address': 'john@example.com'
        })

    @patch('builtins.input', side_effect=['n'])
    @patch('get_mail.store_email_in_database')
    def test_get_email_no_option(self, mock_store_email, mock_input):
        """Testing get_email function when user opts out."""
        get_email()

        # Ensuring the database function is never called when user says 'n'
        mock_store_email.assert_not_called()

    def test_validate_email(self):
        """Testing validate_email with various valid and invalid email addresses."""
        self.assertTrue(validate_email('valid.email@example.com'))
        self.assertTrue(validate_email('valid123@example.co.uk'))
        self.assertFalse(validate_email('invalid-email.com'))
        self.assertFalse(validate_email('invalid-email@com'))
        self.assertFalse(validate_email('invalid@.com'))

    @patch.object(Database, 'add_new_data')
    def test_store_email_in_database_success(self, mock_add_new_data):
        """Testing store_email_in_database when database connection is successful."""
        mock_add_new_data.return_value = None  # Simulating successful database operation
        user_data = {'first_name': 'John', 'email_address': 'john@example.com'}

        try:
            store_email_in_database(user_data)
        except Exception as e:
            self.fail(f"store_email_in_database raised an exception unexpectedly: {e}")

        # Checking that the add_new_data method was called correctly
        mock_add_new_data.assert_called_once_with(
            table_name='emails',
            columns=['first_name', 'email_address'],
            values=('John', 'john@example.com')
        )

    @patch.object(Database, 'add_new_data', side_effect=DbConnectionError("DB connection failed"))
    def test_store_email_in_database_failure(self, mock_add_new_data):
        """Testing store_email_in_database when database connection fails."""
        user_data = {'first_name': 'John', 'email_address': 'john@example.com'}

        # Calling the function and ensure it doesn't raise an exception
        try:
            store_email_in_database(user_data)
        except DbConnectionError:
            self.fail("store_email_in_database() raised DbConnectionError unexpectedly")

        # Ensuring the database function attempted to add data and failed
        mock_add_new_data.assert_called_once_with(
            table_name='emails',
            columns=['first_name', 'email_address'],
            values=('John', 'john@example.com')
        )


if __name__ == '__main__':
    unittest.main()
