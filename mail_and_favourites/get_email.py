from config_joana import HOST, PASSWORD, USER
from db_utils_oli import Database, DbConnectionError
import re
from utils import UserInputCheck


def get_email():
    input_check = UserInputCheck()
    # Looping until the user gives a valid 'yes' or 'no' answer
    wants_email = input_check.get_input("Would you like to receive suggestions via email? (Y/N): ")

    if wants_email == 'y':
        # Looping until a valid name is entered
        while True:
            first_name = input("Please enter your first name: ").strip()
            if first_name.isalpha():
                break  # Valid input received
            else:
                print("Invalid name. Please enter a valid first name (letters only).")

        # Looping until a valid mail_and_favourites address is entered
        while True:
            email_address = input("Please enter your email address: ").strip()
            if validate_email(email_address):
                break  # Valid mail_and_favourites received
            else:
                print("Invalid mail_and_favourites address. Please enter a valid email.")

        # Prepare the data to store in the database
        user_data = {
            'first_name': first_name,
            'email_address': email_address
        }

        # Storing the mail_and_favourites in the database
        store_email_in_database(user_data)

        print("Email sent successfully!")
    else:
        print("Okay, no email will be sent.")


def validate_email(email):
    # Regex to validate mail_and_favourites addresses - it's used to validate the mail_and_favourites address format. It ensures that the mail_and_favourites
    # contains the '@' symbol and follows the general structure of an mail_and_favourites address
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