from dotenv import load_dotenv
import os

load_dotenv()


LOGSTASH_IP = os.getenv("LOGSTASH_IP", "default_logstash_ip")
API_KEY = os.getenv("API_KEY", "default_api_key")
