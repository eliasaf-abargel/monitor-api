import os
import httpx
import asyncio
from datetime import datetime


async def send_log_to_logstash(log_data, retries=3, delay=5):
    logstash_ip = os.getenv("LOGSTASH_IP")
    if not logstash_ip:
        raise Exception("Logstash IP not configured")

    log_data["timestamp"] = datetime.utcnow().isoformat()
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                await client.post(f"http://{logstash_ip}:5055", json=log_data)
            break
        except httpx.RequestError as e:
            if attempt >= retries - 1:
                raise Exception(f"Logstash connection failed: {e}")
            await asyncio.sleep(delay)
