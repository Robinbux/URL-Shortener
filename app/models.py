from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    shortcode = Column(String, index=True)
    created_on = Column(DateTime, default=datetime.datetime.now)
    hits = Column(Integer, default=0)
