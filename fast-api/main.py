from fastapi import FastAPI, HTTPException, Header, Request
from error_schema import ErrorSchema
import config
from security import validate_api_key
from log_handler import send_log_to_logstash
import uvicorn
from datetime import datetime

app = FastAPI()


@app.post("/index-log/{client_name}")
async def report_error(
        request: Request,
        log_data: ErrorSchema,
        client_name: str,
        api_key: str = Header(None),  # API key as a header
):
    # Validate the API key
    if not validate_api_key(api_key, request.url.path):
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Add referer and current UTC timestamp to the log data
    log_data_dict = log_data.dict()
    log_data_dict.update({
        "site_name": client_name,
        "referrer": request.headers.get('referer', 'unknown'),
        "timestamp": datetime.utcnow().isoformat()
    })

    # Send the log data to logstash
    try:
        await send_log_to_logstash(log_data_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "client": client_name}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5001)
