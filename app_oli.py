from flask import Flask, jsonify, request
from db_utils_oli import add_new_data

app = Flask(__name__)


@app.route('/add', methods=['POST'])
def add_details():
    adding = request.get_json()
    add_new_data(
        id=adding['id'],
        name=adding['first_name'],
        email=adding['email_address']
        )
    return adding

if __name__ == '__main__':
    app.run(debug=True, port=5001)