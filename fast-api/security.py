import os

API_KEYS = {
    os.getenv('CAROLINA_API_KEY', 'default_carolina_key'): "/index-log/carolinaui",
    os.getenv('COMAX_API_KEY', 'default_comax_key'): "/index-log/comax",
    os.getenv('WEB_API_KEY', 'default_web_key'): "/index-log/web",
    os.getenv('WS_API_KEY', 'default_ws_key'): "/index-log/ws",
    os.getenv('WS-API_KEY', 'default_ws-api_key'): "/index-log/ws-api",
    os.getenv('RAMI-API_KEY', 'default_rami-api_key'): "/index-log/RAMI-api",
    os.getenv('UMax-API_KEY', 'default_UMax-api_key'): "/index-log/UMax",
    os.getenv('BSB-API_KEY', 'default_BSB-api_key'): "/index-log/BSB",
    os.getenv('BinaPos-API_KEY', 'default_BinaPos-api_key'): "/index-log/BinaPos",
    os.getenv('Comax-App-API_KEY', 'default_Comax-App-api_key'): "/index-log/Comax-App",

}

DEFAULT_KEY = os.getenv("API_KEY", "default-key")


def validate_api_key(api_key, path):
    return api_key in API_KEYS and path.startswith(API_KEYS[api_key]) or api_key == DEFAULT_KEY
