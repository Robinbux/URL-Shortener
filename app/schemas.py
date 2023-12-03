from pydantic import BaseModel, HttpUrl
from datetime import datetime


class URLCreate(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    shortcode: str
    url: HttpUrl
    created_on: datetime


class URLStats(BaseModel):
    hits: int
    url: HttpUrl
    created_on: datetime
