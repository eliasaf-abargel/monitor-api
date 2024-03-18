from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException, Header, Request
from error_schema import ErrorSchema
import config
from security import validate_api_key
from log_handler import send_log_to_logstash
import uvicorn
from datetime import datetime

app = FastAPI()

# Add CORSMiddleware to allow all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Add a route to report errors
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
        "timestamp": datetime.utcnow().isoformat()
    })

    # Send the log data to logstash
    try:
        if "message" in log_data_dict and log_data_dict["message"]:
            await send_log_to_logstash(log_data_dict)
        elif "messages" in log_data_dict and log_data_dict["messages"]:
            messages = log_data_dict["messages"]
            del log_data_dict["messages"]
            for message in messages:
                log_data_dict["message"] = message
                await send_log_to_logstash(log_data_dict)
        else:
             raise Exception("No message in log data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "client": client_name}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5001)
