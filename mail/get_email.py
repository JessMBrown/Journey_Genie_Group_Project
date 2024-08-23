from config import HOST, PASSWORD, USER
from database.db_utils_oli import Database, DbConnectionError
import re
from utils import UserInputCheck


def get_email():
    input_check = UserInputCheck()
    # Looping until the user gives a valid 'yes' or 'no' answer
<<<<<<<< HEAD:userEmail/get_email.py
    wants_email = input_check.get_input("Would you like to receive suggestions via userEmail? (Y/N): ")
========
    wants_email = input_check.get_input("Would you like to receive suggestions via mail? (Y/N): ")
>>>>>>>> joana_branch:mail/get_email.py

    if wants_email == 'y':
        # Looping until a valid name is entered
        while True:
            first_name = input("Please enter your first name: ").strip()
            if first_name.isalpha():
                break  # Valid input received
            else:
                print("Invalid name. Please enter a valid first name (letters only).")

<<<<<<<< HEAD:userEmail/get_email.py
        # Looping until a valid userEmail address is entered
        while True:
            email_address = input("Please enter your userEmail address: ").strip()
            if validate_email(email_address):
                break  # Valid userEmail received
            else:
                print("Invalid userEmail address. Please enter a valid userEmail.")
========
        # Looping until a valid mail address is entered
        while True:
            email_address = input("Please enter your mail address: ").strip()
            if validate_email(email_address):
                break  # Valid mail received
            else:
                print("Invalid mail address. Please enter a valid mail.")
>>>>>>>> joana_branch:mail/get_email.py

        # Prepare the data to store in the database
        user_data = {
            'first_name': first_name,
            'email_address': email_address
        }

<<<<<<<< HEAD:userEmail/get_email.py
        # Storing the userEmail in the database
========
        # Storing the mail in the database
>>>>>>>> joana_branch:mail/get_email.py
        store_email_in_database(user_data)

        print("Email sent successfully!")
    else:
<<<<<<<< HEAD:userEmail/get_email.py
        print("Okay, no userEmail will be sent.")


def validate_email(email):
    # Regex to validate userEmail addresses - it's used to validate the userEmail address format. It ensures that the userEmail
    # contains the '@' symbol and follows the general structure of an userEmail address
========
        print("Okay, no mail will be sent.")


def validate_email(email):
    # Regex to validate mail addresses - it's used to validate the mail address format. It ensures that the mail
    # contains the '@' symbol and follows the general structure of an mail address
>>>>>>>> joana_branch:mail/get_email.py
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
<<<<<<<< HEAD:userEmail/get_email.py
        print(f"Failed to store userEmail in the database: {e}")
========
        print(f"Failed to store mail in the database: {e}")
>>>>>>>> joana_branch:mail/get_email.py
