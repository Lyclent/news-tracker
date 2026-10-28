from pydantic import BaseModel
from datetime import datetime

class NewsOut(BaseModel):
    id: int
    title: str
    link: str
    source: str
    publisher_at: datetime
    sentiment: str | None
    sentiment_score: float | None

    class Config:
        from_attributes = True