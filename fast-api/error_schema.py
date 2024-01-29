import json
import jsonschema


def validate_error_schema(log_data):
    try:
        with open('error_schema.json', 'r') as schema_file:
            error_report_schema = json.load(schema_file)
        jsonschema.validate(instance=log_data, schema=error_report_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise Exception(f"Schema validation error: {e}")
