from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from database import Base

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    link = Column(String, unique=True, nullable=False)
    sourse = Column(String, nullable=False)
    published_at = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String, nullable=True)
    sentiment_core = Column(Float, nullable=True)

    