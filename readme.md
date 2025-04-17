# Stock News Scraper Microservice

A FastAPI-based microservice that scrapes, filters, and summarizes stock and market-related news articles for a specified company. The service uses SerpAPI for news searches, Playwright for web scraping, CrewAI for summarization, and MongoDB for persistent storage. It follows a **Model-View-Service (MVS)** architecture for modularity and maintainability.

## Features
- **Search**: Queries SerpAPI to find recent stock news for a given company.
- **Scrape**: Extracts article content using Playwright.
- **Filter**: Ensures articles are stock or market-related based on keywords.
- **Summarize**: Generates a concise summary (150-200 words) of relevant articles using CrewAI and OpenAI's GPT-4o-mini.
- **Store**: Saves articles to MongoDB for persistence.
- **API**: Provides RESTful endpoints to fetch news and summaries.

## Tech Stack
- **Python**: 3.10+ (3.9 supported with CrewAI 0.30.11)
- **FastAPI**: For building the REST API
- **CrewAI**: For agent-based summarization
- **Playwright**: For web scraping
- **SerpAPI**: For news search
- **MongoDB**: For data storage
- **Pydantic**: For data validation
- **FAISS**: As the vector store for CrewAI

## Project Structure
```
stock_news_scraper/
├── models/                 # Data models (Pydantic)
│   ├── __init__.py
│   ├── article.py         # News article model
│   └── request_response.py # Request/response models
├── services/               # Business logic
│   ├── __init__.py
│   ├── news_service.py    # News search logic
│   ├── scraper_service.py # Web scraping logic
│   ├── filter_service.py  # Article filtering logic
│   ├── summarizer_service.py # Summarization logic
│   └── database_service.py # MongoDB operations
├── views/                  # API endpoints
│   ├── __init__.py
│   └── api.py            # FastAPI routes
├── utils/                  # Utilities and configuration
│   ├── __init__.py
│   ├── config.py         # Environment variables
│   └── logger.py         # Logging setup
├── main.py                # Entry point
├── requirements.txt       # Dependencies
└── .env                   # Environment variables (not tracked)
```

## Prerequisites
- **Python**: 3.10 or higher (3.9 supported with CrewAI downgrade)
- **MongoDB**: Local instance or cloud (e.g., MongoDB Atlas)
- **API Keys**:
  - [OpenAI API Key](https://platform.openai.com/) for CrewAI
  - [SerpAPI Key](https://serpapi.com/) for news searches

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/stock-news-scraper.git
cd stock-news-scraper
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install faiss-cpu  # For CrewAI vector store
playwright install     # Install Playwright browsers
```

**Note**: If using Python 3.9, downgrade CrewAI due to compatibility issues:
```bash
pip install crewai==0.30.11
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key
SERPAPI_KEY=your_serpapi_key
MONGO_URI=your_mongo_uri
```
- Replace `your_openai_api_key` with your OpenAI API key.
- Replace `your_serpapi_key` with your SerpAPI key.
- Replace `your_mongo_uri` with your MongoDB connection string (e.g., `mongodb://localhost:27017` or MongoDB Atlas URI).

### 5. Run the Application
```bash
python main.py
```
You should see output like:
```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```

The API will be available at `http://localhost:8000`.

## Usage

### API Endpoints
- **Health Check**
  ```
  GET /health
  ```
  **Response**:
  ```json
  {"status": "healthy"}
  ```

- **Get Company News**
  ```
  POST /news
  Content-Type: application/json
  ```
  **Request Body**:
  ```json
  {"company": "Apple"}
  ```
  **Response**:
  ```json
  {
    "company": "Apple",
    "articles": [
      {
        "id": "uuid",
        "company": "Apple",
        "title": "Apple Stock Rises After Earnings",
        "url": "https://example.com/news",
        "content": "Apple reported strong Q2 earnings...",
        "published_date": "2025-04-15",
        "source": "Example News",
        "scraped_at": "2025-04-17T12:34:56Z"
      },
      ...
    ],
    "summary": "Apple's stock rose 3% following strong Q2 earnings, driven by iPhone sales and services growth. Analysts remain bullish..."
  }
  ```

### Example with cURL
```bash
curl -X POST http://localhost:8000/news -H "Content-Type: application/json" -d '{"company": "Apple"}'
```

## Troubleshooting

### Issue: `python main.py` Goes to Next Line Without Output
If the script exits silently:
1. **Check Python Version**:
   ```bash
   python --version
   ```
   Ensure Python 3.10+ (or downgrade CrewAI for 3.9).
2. **Verify Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install faiss-cpu
   playwright install
   ```
3. **Test Imports**:
   ```bash
   python -c "from views.api import router; from utils.logger import setup_logging; print('Imports OK')"
   ```
4. **Add Debug Prints** in `main.py`:
   ```python
   print("Starting script...")
   if __name__ == "__main__":
       print("Running Uvicorn...")
       uvicorn.run(app, host="localhost", port=8000, log_level="debug")
   ```
5. **Check Port**:
   Ensure port 8000 is free:
   ```bash
   lsof -i :8000
   ```
   Change to 8001 if needed.

### Issue: Dependency Errors (e.g., `hnswlib`, `chroma-hnswlib`)
- Install build tools:
  ```bash
  sudo apt install build-essential python3-dev
  ```
- Use FAISS:
  ```bash
  pip install faiss-cpu
  ```

### Issue: MongoDB Connection Failure
- Verify `MONGO_URI` in `.env`.
- Test connection:
  ```bash
  python -c "from pymongo import MongoClient; client = MongoClient('your_mongo_uri'); print('Connected')"
  ```

### Issue: API Key Errors
- Ensure `OPENAI_API_KEY` and `SERPAPI_KEY` are valid.
- Test SerpAPI:
  ```bash
  python -c "from serpapi import GoogleSearch; print(GoogleSearch({'q': 'test', 'api_key': 'your_serpapi_key'}).get_dict())"
  ```

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For issues or questions, open an issue on GitHub or contact [ritankar.jana.official@gmail.com].