from fastapi import APIRouter, HTTPException
from models.request_response import CompanyRequest, NewsResponse
from models.articles import NewsArticle
from services.news_service import search_news
from services.scraper_service import scrape_article
from services.filter_service import filter_stock_related
from services.summarizer_service import summarize_articles
from services.database_service import DatabaseService
from typing import List
from uuid import uuid4
from datetime import datetime
from utils.logger import logger
import asyncio

router = APIRouter()

async def scrape_news(company: str) -> tuple[List[dict], str]:
    """
    Scrape, filter, and summarize news articles for a company.
    
    Args:
        company: Name of the company.
    
    Returns:
        Tuple of filtered articles and their summary.
    """
    db_service = DatabaseService()
    try:
        # Search for articles
        articles = await search_news(company)
        if not articles:
            return [], "No relevant news articles found."

        # Scrape articles in parallel
        contents = await asyncio.gather(*(scrape_article(article["url"]) for article in articles))

        # Filter and store relevant articles
        filtered_articles = []
        for article, content in zip(articles, contents):
            if content and filter_stock_related(content):
                article_id = str(uuid4())
                article_data = {
                    "id": article_id,
                    "company": company,
                    "title": article["title"],
                    "url": article["url"],
                    "content": content,
                    "published_date": article["published_date"],
                    "source": article["source"],
                    "scraped_at": datetime.utcnow()
                }
                db_service.insert_article(article_data)
                filtered_articles.append(article_data)

        # Generate summary
        summary = summarize_articles(company, filtered_articles) if filtered_articles else "No relevant news articles found."

        return filtered_articles, summary
    finally:
        db_service.close()

@router.post("/news", response_model=NewsResponse)
async def get_company_news(request: CompanyRequest):
    """
    Fetch and summarize latest stock news for a company.
    
    Args:
        request: CompanyRequest containing the company name.
    
    Returns:
        NewsResponse with articles and summary.
    
    Raises:
        HTTPException: If no news is found or an error occurs.
    """
    try:
        articles, summary = await scrape_news(request.company)
        if not articles:
            raise HTTPException(status_code=404, detail=f"No stock news found for {request.company}")

        return NewsResponse(
            company=request.company,
            articles=[
                NewsArticle(
                    id=article["id"],
                    company=article["company"],
                    title=article["title"],
                    url=article["url"],
                    content=article["content"],
                    published_date=article["published_date"],
                    source=article["source"],
                    scraped_at=article["scraped_at"]
                )
                for article in articles
            ],
            summary=summary
        )
    except Exception as e:
        logger.error(f"Error processing request for {request.company}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}