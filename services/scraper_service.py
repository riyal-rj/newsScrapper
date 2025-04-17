from playwright.async_api import async_playwright
from utils.logger import logger

async def scrape_article(url: str) -> str:
    """
    Scrape article content using Playwright.
    
    Args:
        url: URL of the article to scrape.
    
    Returns:
        Extracted text content of the article (limited to 2000 characters).
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=30000)
            content = await page.evaluate(
                """() => {
                    const selectors = ['article', '.article-body', 'main', '.content'];
                    for (const selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element) return element.innerText;
                    }
                    return document.body.innerText;
                }"""
            )
            await browser.close()
            return content.strip()[:2000]
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        return ""