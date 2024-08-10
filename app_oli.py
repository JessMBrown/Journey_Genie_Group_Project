from flask import Flask, jsonify, request
from db_utils_oli import Database, DbConnectionError
from config_oli import USER, PASSWORD, HOST

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


if __name__ == '__main__':
    app.run(debug=True, port=5001)