import unittest
from unittest.mock import patch, MagicMock
from db_utils import Database, DbConnectionError


class TestDatabase(unittest.TestCase):

    @patch('db_utils.mysql.connector.connect')
    def setUp(self, mock_connect):
        # Mocking the database connection - used mocking to avoid real database connections
        self.mock_connection = MagicMock()
        mock_connect.return_value = self.mock_connection
        self.db = Database('host', 'user', 'password', 'db_name')

    def test_add_new_data_success(self):
        table_name = 'test_table'
        columns = ['column1', 'column2']
        values = ('value1', 'value2')

        self.db.add_new_data(table_name, columns, values)

        # Ensuring the query was executed with the correct SQL command
        self.db.cursor.execute.assert_called_with(
            "INSERT INTO test_table (column1, column2) VALUES (%s, %s)",
            values
        )
        self.mock_connection.commit.assert_called_once()

    def test_add_new_data_failure(self):
        # Simulating a generic exception during data insertion
        self.db.cursor.execute.side_effect = Exception("Simulated insert error")

        with self.assertRaises(DbConnectionError):
            self.db.add_new_data('test_table', ['column1', 'column2'], ('value1', 'value2'))

        # Ensuring the commit was not called due to the error
        self.mock_connection.commit.assert_not_called()

    def test_fetch_data_success(self):
        table_name = 'test_table'
        columns = ['column1', 'column2']
        conditions = "column1 = 'value1'"

        # Mocking the results of the query
        self.db.cursor.fetchall.return_value = [('value1', 'value2')]

        results = self.db.fetch_data(table_name, columns, conditions)

        self.db.cursor.execute.assert_called_with(
            "SELECT column1, column2 FROM test_table WHERE column1 = 'value1'"
        )
        self.assertEqual(results, [('value1', 'value2')])

    def test_fetch_data_failure(self):
        # Simulating a generic exception during data fetching
        self.db.cursor.execute.side_effect = Exception("Simulated fetch error")

        with self.assertRaises(DbConnectionError):
            self.db.fetch_data('test_table')

    def test_close(self):
        self.db.close()

        # Ensuring that both cursor and connection are closed
        self.db.cursor.close.assert_called_once()
        self.mock_connection.close.assert_called_once()

    def tearDown(self):  # used to clean up resources after the tests
        if self.db.connection.is_connected():
            self.db.connection.close()


if __name__ == '__main__':
    unittest.main()
