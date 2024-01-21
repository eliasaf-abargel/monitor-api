import json
from datetime import datetime
import jsonschema
from flask import Flask, request, jsonify
from jsonschema import validate

app = Flask(__name__)

API_KEY = 'JY8LVI4fQNS-raAnzs5Y4Q'

# Load the JSON schema for the error reports from an external file
with open('error_schema.json', 'r') as schema_file:
    error_report_schema = json.load(schema_file)


def is_valid_date(timestamp):
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False


@app.route('/report_error', methods=['POST'])
def report_error():
    api_key = request.headers.get('API-Key')

    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    error_data = request.json

    try:
        validate(instance=error_data, schema=error_report_schema)

        if not is_valid_date(error_data["timestamp"]):
            raise ValueError("Invalid timestamp format.")

    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400

    with open('error_log.json', 'a') as file:
        json.dump(error_data, file)
        file.write('\n')

    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
