from pydantic import BaseModel
from typing import Optional


class RequestModel(BaseModel):
    method: str
    body_bytes: int


class ErrorSchema(BaseModel):
    log_type: str
    message:Optional[str] = None
    environment:Optional[str] = None
    messages:Optional[list[str]] = None


