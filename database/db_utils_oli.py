import mysql.connector


class DbConnectionError(Exception):
    pass


class Database:
    def __init__(self, host, user, password, db_name):
        """Initializing the database connection."""
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.cursor = self.connection.cursor()

    def add_new_data(self, table_name, columns, values):
        """Inserting data into any specified table."""
        try:
            # Formulating the query
            columns_str = ', '.join(columns)  # variable is a string of column names joined by commas
            placeholders = ', '.join(['%s'] * len(values))  # variable is a string of %s placeholders for each value,
            # also joined by commas. Safety thing - using parameterized queries (%s placeholders) prevents SQL
            # injection attacks
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

            # Executing the query with provided values
            self.cursor.execute(query, values)
            self.connection.commit()

            print("New data added successfully")

        except Exception:
            raise DbConnectionError("Failed to write data to DB")

        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                # print("DB connection is closed")

    def fetch_data(self, table_name, columns='*', conditions=None, join=None):
        """Fetching data from any specified table."""
        try:
            # Formulating the query - the same method can handle simple SELECT * queries as well as more complex
            # queries with multiple conditions.
            columns_str = ', '.join(columns) if isinstance(columns, list) else columns
            query = f"SELECT {columns_str} FROM {table_name}"  # The columns parameter can be a list of columns
            # or a string '*' to fetch all columns.

            if join:
                query += f" {join}"  # this will allow us to join the tables when necessary

            # Add conditions if provided
            if conditions:
                query += f" WHERE {conditions}"  # The conditions parameter is an optional string where you can specify
                # conditions for the query

            # Executing the query and fetch the results
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            return results

        except Exception:
            raise DbConnectionError("Failed to fetch data from DB")

        # the "finally" block has been commented out as it was causing issues with accessing the database in functions
        # which have been created later
        # finally:
        #     if self.connection.is_connected():
        #         self.cursor.close()
        #         self.connection.close()
        #         print("DB connection is closed")

    def close(self):
        """Closing the database connection."""
        self.cursor.close()
        self.connection.close()
