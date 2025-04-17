from pydantic import BaseModel
from typing import List
from .articles import NewsArticle

class CompanyRequest(BaseModel):
    """Request model for company news."""
    company: str

class NewsResponse(BaseModel):
    """Response model for news articles and summary."""
    company: str
    articles: List[NewsArticle]
    summary: str