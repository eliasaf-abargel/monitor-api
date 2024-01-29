from fastapi import FastAPI, HTTPException, Header
import config
from log_handler import send_log_to_logstash
from error_schema import validate_error_schema
from security import validate_api_key
import uvicorn

app = FastAPI()


@app.post('/index-log')
async def report_error(log_data: dict, api_key: str = Header(None)):
    if not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        validate_error_schema(log_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        await send_log_to_logstash(log_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5001)
