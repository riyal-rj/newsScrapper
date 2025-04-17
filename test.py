import os
from serpapi import  GoogleSearch
import dotenv

dotenv.load_dotenv()
os.environ["SERPAPI_KEY"] = "b7c5a670da92b40c6cd69cbfd990b03baafcbc679aa4c8c4c48a6bbfd1bb539e"

params = {
    "q": "Tesla stock news",
    "tbm": "nws",
    "api_key": os.getenv("SERPAPI_KEY")
}

search = GoogleSearch(params)
results = search.get_dict()
for result in results.get("news_results", []):
    print(result["title"], result["link"])