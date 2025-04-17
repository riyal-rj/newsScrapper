from typing import List, Dict, Tuple
from serpapi import GoogleSearch
from utils.config import SERPAPI_KEY
from utils.logger import logger

async def search_news(company: str) -> List[Dict]:
    """
    Search for news articles using SerpAPI.
    
    Args:
        company: Name of the company to search for.
    
    Returns:
        List of dictionaries containing article metadata (title, url, source, date).
    """
    try:
        params = {
            "q": f"{company} stock news",
            "tbm": "nws",
            "api_key": SERPAPI_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict().get("news_results", [])
        return [
            {
                "title": result["title"],
                "url": result["link"],
                "source": result.get("source", "Unknown"),
                "published_date": result.get("date", "Unknown")
            }
            for result in results
        ]
    except Exception as e:
        logger.error(f"Error searching news for {company}: {str(e)}")
        return []