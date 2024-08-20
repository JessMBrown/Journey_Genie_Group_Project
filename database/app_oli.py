from flask import Flask, jsonify, request
from database.db_utils_oli import Database, DbConnectionError
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



if __name__ == '__main__':
    app.run(debug=True, port=5001)
