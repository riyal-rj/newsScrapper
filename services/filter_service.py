def filter_stock_related(content: str) -> bool:
    """
    Check if article content is stock or market-related based on keywords.
    
    Args:
        content: Text content of the article.
    
    Returns:
        Boolean indicating if the content is stock or market-related.
    """
    keywords = [
        "stock", "market", "shares", "earnings", "dividend", "ipo",
        "financial", "revenue", "profit", "loss", "bullish", "bearish"
    ]
    return any(keyword.lower() in content.lower() for keyword in keywords)