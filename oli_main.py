from config_oli import HOST, PASSWORD, USER
from db_utils_oli import Database, DbConnectionError
import re


def get_email():
    # Looping until the user gives a valid 'yes' or 'no' answer
    while True:
        wants_email = input("Would you like to receive suggestions via email? (yes/no): ").strip().lower()

        if wants_email in ['yes', 'no']:
            break  # Valid input received
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    if wants_email == 'yes':
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
    # Regex to validate email addresses - it's used to validate the email address format. It ensures that the email
    # contains the '@' symbol and follows the general structure of an email address
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
