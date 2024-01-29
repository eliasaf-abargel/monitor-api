import os

API_KEY = os.environ.get("API_KEY", "default-key")


def validate_api_key(api_key):
    return api_key == API_KEY
