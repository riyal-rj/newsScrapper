import uvicorn
from fastapi import FastAPI
from views.api import router as api_router
from utils.logger import setup_logging

# Initialize logging
setup_logging()

# Initialize FastAPI app
app = FastAPI(title="Stock News Scraper Microservice")

# Include API routes
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)