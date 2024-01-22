import json
import os
from datetime import datetime
import jsonschema
from flask import Flask, request, jsonify
from jsonschema import validate
import requests  # for sending data to Logstash

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "JY8LVI4fQNS-raAnzs5Y4Q")  # Fallback to a default

# Load the schema outside of the route to avoid repeated file reads.
try:
    with open('error_schema.json', 'r') as schema_file:
        error_report_schema = json.load(schema_file)
except Exception as e:
    print(f"Error loading schema: {e}")
    exit(1)

@app.route('/index-log', methods=['POST'])
def report_error():
    api_key = request.headers.get("API-Key")

    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    log_data = request.json

    try:
        validate(instance=log_data, schema=error_report_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400

    log_data["timestamp"] = datetime.utcnow().isoformat()

    # Save log data to file
    try:
        with open('error_log.json', 'a') as file:
            file.write(json.dumps(log_data) + '\n')
    except IOError as e:
        return jsonify({"error": "Failed to write to log file", "message": str(e)}), 500

    # Send log data to Logstash
    try:
        requests.post("http://192.168.203.34:5055", json=log_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Logstash Connection Failed", "message": str(e)}), 500

    return jsonify(dict(status="success")), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
