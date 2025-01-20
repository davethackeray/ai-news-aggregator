from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsItem(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    source: str
    interesting_score: float
    published_at: datetime
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True