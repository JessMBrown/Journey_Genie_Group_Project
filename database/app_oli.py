from flask import Flask, jsonify, request
from db_utils_oli import Database, DbConnectionError
from config_oli import USER, PASSWORD, HOST
import mysql
from mysql import connector

app = Flask(__name__)


@app.route('/add', methods=['POST'])
def add_details():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='customer_details')
    try:
        # Getting data from the POST request
        adding = request.get_json()

        # Calling the add_new_data method
        db.add_new_data(
            table_name='emails',  # Specifying the table name
            columns=['id', 'first_name', 'email_address'],  # Specifying the columns
            values=(adding['id'], adding['first_name'], adding['email_address'])  # Passing the values as a tuple
        )

        return jsonify({'status': 'success', 'data': adding}), 200

    except DbConnectionError as e:  # to handle database connection issues
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except KeyError as e:  # to handle cases where the JSON is missing required keys
        return jsonify({'status': 'error', 'message': f'Missing key: {str(e)}'}), 400

    except Exception as e:  # to catch any other issues
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/view/countries', methods=['GET'])
def get_countries():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        table_name = 'countries'
        columns = ['DISTINCT countries.country_name']
        join = "INNER JOIN cities ON countries.country_code = cities.country_code"
        conditions = request.args.get('conditions')

        data = db.fetch_data(
            table_name=table_name,
            columns=columns,
            join=join,
            conditions=conditions
        )

        # Returning the fetched data as JSON
        return jsonify({'status': 'success', 'data': data}), 200

    except DbConnectionError as e:  # Handle database connection issues
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except Exception as e:  # Catch any other issues
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/view/cities', methods=['GET'])
def get_cities():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        table_name = 'cities'
        columns = ['DISTINCT city_name']
        join = None
        # Collecting all conditions and join them with ' AND '
        conditions_list = request.args.getlist('conditions')
        conditions = ' AND '.join(conditions_list) if conditions_list else None

        data = db.fetch_data(
            table_name=table_name,
            columns=columns,
            join=join,
            conditions=conditions
        )

        # Returning the fetched data as JSON
        return jsonify({'status': 'success', 'data': data}), 200

    except DbConnectionError as e:  # Handle database connection issues
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except Exception as e:  # Catch any other issues
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/view/favourite_hotels', methods=['GET'])
def get_favourite_hotels():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        table_name = 'favourite_hotels'
        columns = ['fav_hotel_ID', 'hotel_name', 'city_ID', 'country_code', 'favourite_date']
        conditions = request.args.get('conditions')

        data = db.fetch_data(
            table_name=table_name,
            columns=columns,
            conditions=conditions,
        )

        return jsonify({'status': 'success', 'data': data}), 200

    except DbConnectionError as e:
        print(f"DbConnectionError: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Fetching favorite activities
@app.route('/view/favourite_activities', methods=['GET'])
def get_favourite_activities():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        table_name = 'favourite_activities'
        columns = ['activity_ID', 'activity_name', 'city_ID', 'country_code', 'favourite_date']
        conditions = request.args.get('conditions')

        data = db.fetch_data(
            table_name=table_name,
            columns=columns,
            conditions=conditions
        )

        return jsonify({'status': 'success', 'data': data}), 200

    except DbConnectionError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Add favorite hotel
@app.route('/add/favourite_hotel', methods=['POST'])
def add_favourite_hotel():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        # Getting data from the POST request
        adding = request.get_json()

        # Calling the add_new_data method
        db.add_new_data(
            table_name='favourite_hotels',
            columns=['fav_hotel_ID', 'hotel_name', 'city_ID', 'country_code', 'favourite_date'],
            values=(
                adding['fav_hotel_ID'],
                adding['hotel_name'],
                adding['city_ID'],
                adding['country_code'],
                adding['favourite_date']
            )
        )

        return jsonify({'status': 'success', 'data': adding}), 200

    except DbConnectionError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'Missing key: {str(e)}'}), 400

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Add favorite activity
@app.route('/add/favourite_activities', methods=['POST'])
def add_favourite_activities():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        entries = request.get_json()

        if isinstance(entries, dict):
            entries = [entries]

        for entry in entries:
            # Attempting to insert the data into the database
            db.add_new_data(
                table_name='favourite_activities',
                columns=['activity_ID', 'activity_name', 'city_ID', 'country_code', 'favourite_date'],
                values=(
                    entry.get('activity_ID'),
                    entry.get('activity_name'),
                    entry.get('city_ID'),
                    entry.get('country_code'),
                    entry.get('favourite_date')
                )
            )

        return jsonify({'status': 'success', 'data': entries}), 200

    except mysql.connector.Error as err:
        # Log the specific MySQL error
        print(f"MySQL Error: {err}")
        return jsonify({'status': 'error', 'message': f"Database error: {err}"}), 500

    except DbConnectionError as e:
        print(f"DbConnectionError: {str(e)}")  # Debugging: log the DB connection error
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except KeyError as e:
        print(f"KeyError: Missing key: {str(e)}")  # Debugging: log missing keys
        return jsonify({'status': 'error', 'message': f'Missing key: {str(e)}'}), 400

    except Exception as e:
        print(f"Unhandled Exception: {str(e)}")  # Debugging: log any other unhandled exceptions
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
