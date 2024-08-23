from flask import Flask, jsonify, request
from db_utils_oli import Database, DbConnectionError
from config import USER, PASSWORD, HOST

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
        columns = ['favourite_hotels.hotel_name']
        join = None
        conditions = request.args.get('hotel_ID = ')

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


@app.route('/view/favourite_activities', methods=['GET'])
def get_favourite_activities():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        table_name = 'favourite_activities'
        columns = ['favourite_activities.kinds']
        join = None
        conditions = request.args.get('activity_ID = ')

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


@app.route('/add_favourite_hotels', methods=['POST'])
def add_favourite_hotels():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        # Getting data from the POST request
        adding = request.get_json()

        # Calling the add_new_data method
        db.add_new_data(
            table_name='favourite_hotels',  # Specifying the table name
            columns=['fav_hotel_ID', 'hotel_name', 'city_ID', 'country_code', 'favourited_date'],  # Specifying the columns
            values=(adding['hotel_id'], adding['hotel_name'], adding['city_ID'], adding['country_code'], adding['favourited_date'])  # Passing the values as a tuple
        )

        return jsonify({'status': 'success', 'data': adding}), 200

    except DbConnectionError as e:  # to handle database connection issues
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except KeyError as e:  # to handle cases where the JSON is missing required keys
        return jsonify({'status': 'error', 'message': f'Missing key: {str(e)}'}), 400

    except Exception as e:  # to catch any other issues
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/add_favourite_activities', methods=['POST'])
def add_favourite_activities():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        # Getting data from the POST request
        adding = request.get_json()

        # Calling the add_new_data method
        db.add_new_data(
            table_name='favourite_activities',  # Specifying the table name
            columns=['activity_ID', 'activity_name', 'city_ID', 'country_code', 'favourited_date'], # Specifying the columns
            values=(adding['activity_ID'], adding['activity_name'], adding['city_ID'],
                    adding['country_code'],adding['favourited_date'])  # Passing the values as a tuple
        )

        return jsonify({'status': 'success', 'data': adding}), 200

    except DbConnectionError as e:  # to handle database connection issues
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except KeyError as e:  # to handle cases where the JSON is missing required keys
        return jsonify({'status': 'error', 'message': f'Missing key: {str(e)}'}), 400

    except Exception as e:  # to catch any other issues
        return jsonify({'status': 'error', 'message': str(e)}), 500



@app.route('/view/favourite_hotels/<int:hotel_id>', methods=['GET'])
def get_favourite_hotels(hotel_id):
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        table_name = 'favourite_hotels'
        columns = ['hotel_name', 'favourite_date']
        conditions = f' hotel_ID = {hotel_id}'
        join = None

        data = db.fetch_data(
            table_name=table_name,
            columns=columns,
            conditions=conditions,
            join=join
        )

        # Returning the fetched data as JSON
        return jsonify({'status': 'success', 'data': data}), 200

    except DbConnectionError as e:  # Handle database connection issues
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except Exception as e:  # Catch any other issues
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/view/favourite_activities/<int:activity_id>', methods=['GET'])
def get_favourite_activities(activity_id):
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        table_name = 'favourite_activities'
        columns = ['kinds']
        join = None
        conditions = f' activity_ID = {activity_id}'

        data = db.fetch_data(
            table_name=table_name,
            columns=columns,
            conditions=conditions,
            join=join
        )

        # Returning the fetched data as JSON
        return jsonify({'status': 'success', 'data': data}), 200

    except DbConnectionError as e:  # Handle database connection issues
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except Exception as e:  # Catch any other issues
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/add/favourite_hotels', methods=['POST'])
def add_favourite_hotels():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        # Getting data from the POST request
        adding = request.get_json()

        # Calling the add_new_data method
        db.add_new_data(
            # Specifying the table name
            table_name='favourite_hotels',
            # Specifying the columns
            columns=['fav_hotel_name', 'city_ID', 'country_code', 'favourite_date'],
            # Passing the values as a tuple
            values=(adding['fav_hotel_name'], adding['city_ID'], adding['country_code'], adding['favourite_date'])
        )

        return jsonify({'status': 'success', 'data': adding}), 200

    except DbConnectionError as e:  # to handle database connection issues
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except KeyError as e:  # to handle cases where the JSON is missing required keys
        return jsonify({'status': 'error', 'message': f'Missing key: {str(e)}'}), 400

    except Exception as e:  # to catch any other issues
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/add/favourite_activities', methods=['POST'])
def add_favourite_activities():
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
    try:
        # Getting data from the POST request
        adding = request.get_json()

        # Calling the add_new_data method
        db.add_new_data(
            table_name='favourite_activities',  # Specifying the table name
            columns=['city_ID', 'country_code', 'favourite_date'],  # Specifying the columns
            values=(adding['city_ID'], adding['country_code'], adding['favourite_date'])  # Passing the values as a tuple
        )

        return jsonify({'status': 'success', 'data': adding}), 200

    except DbConnectionError as e:  # to handle database connection issues
        return jsonify({'status': 'error', 'message': str(e)}), 500

    except KeyError as e:  # to handle cases where the JSON is missing required keys
        return jsonify({'status': 'error', 'message': f'Missing key: {str(e)}'}), 400

    except Exception as e:  # to catch any other issues
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)


if __name__ == '__main__':
    app.run(debug=True, port=5001)

