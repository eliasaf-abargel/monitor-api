from datetime import datetime
import os
import httpx  # Using httpx for async HTTP requests


async def send_log_to_logstash(log_data):
    log_data["timestamp"] = datetime.utcnow().isoformat()

    logstash_ip = os.environ.get("LOGSTASH_IP")
    if not logstash_ip:
        raise Exception("Logstash IP not configured in .env file")

    try:
        # Send log data to Logstash
        async with httpx.AsyncClient() as client:
            await client.post(f"http://{logstash_ip}:5055", json=log_data)
    except httpx.RequestError as e:
        raise Exception(f"Logstash Connection Failed: {e}")
