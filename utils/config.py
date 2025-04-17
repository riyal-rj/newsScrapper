import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "stock_news"
COLLECTION_NAME = "articles"

# Set FAISS as vector store
os.environ["CREWAI_VECTOR_STORE"] = "faiss"