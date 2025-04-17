from pymongo import MongoClient
from utils.config import MONGO_URI, DB_NAME, COLLECTION_NAME
from typing import Dict

class DatabaseService:
    """Service for interacting with MongoDB."""
    
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]
    
    def insert_article(self, article: Dict) -> None:
        """
        Insert an article into the MongoDB collection.
        
        Args:
            article: Dictionary containing article data.
        """
        self.collection.insert_one(article)
    
    def close(self) -> None:
        """Close the MongoDB client connection."""
        self.client.close()