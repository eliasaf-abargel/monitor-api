from pydantic import BaseModel, HttpUrl, IPvAnyAddress
from typing import Optional


class RequestModel(BaseModel):
    method: str
    body_bytes: int


class ErrorSchema(BaseModel):
    log_type: str
    message: str
    client_ip: Optional[IPvAnyAddress] = None
    user_agent: Optional[str] = None
    referrer: Optional[HttpUrl] = None
    site_name: str
    url: HttpUrl
    request: RequestModel

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        if d.get('url', None) is not None:
            d['url'] = str(d['url'])
        if d.get('referrer', None) is not None:
            d['referrer'] = str(d['referrer']) if d['referrer'] is not None else None
        return d
