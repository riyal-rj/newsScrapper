from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsArticle(BaseModel):
    """Model for a single news article."""
    id: str
    company: str
    title: str
    url: str
    content: str
    published_date: str
    source: str
    scraped_at: Optional[datetime] = None