from database.config_oli import HOST, PASSWORD, USER
from database.db_utils_oli import Database, DbConnectionError
from utils import UserInputCheck
import re


def get_email():
    input_check = UserInputCheck()

    # Checking if the user wants to receive email
    wants_email = input_check.get_input("Would you like to receive suggestions via email? (y/n): ")

    if wants_email == 'y':
        # Looping until a valid name is entered
        while True:
            first_name = input("Please enter your first name: ").strip()
            if first_name.isalpha():
                break  # Valid input received
            else:
                print("Invalid name. Please enter a valid first name (letters only).")

        # Looping until a valid email address is entered
        while True:
            email_address = input("Please enter your email address: ").strip()
            if validate_email(email_address):
                break  # Valid email received
            else:
                print("Invalid email address. Please enter a valid email.")

        # Prepare the data to store in the database
        user_data = {
            'first_name': first_name,
            'email_address': email_address
        }

        # Storing the email in the database
        store_email_in_database(user_data)

        print("Email sent successfully!")
    else:
        print("Okay, no email will be sent.")


def validate_email(email):
    # Regex to validate email addresses
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


def store_email_in_database(user_data):
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='customer_details')

    try:
        # Assuming there's an auto-increment 'id' in the table
        db.add_new_data(
            table_name='emails',
            columns=['first_name', 'email_address'],
            values=(user_data['first_name'], user_data['email_address'])
        )
    except DbConnectionError as e:
        print(f"Failed to store email in the database: {e}")