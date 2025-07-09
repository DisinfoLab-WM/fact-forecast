import pyrebase
import json
import logging
import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Firebase configuration from environment variables
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET")
}

class FirebaseClient:
    def __init__(self):
        logger.info("Initializing Firebase client")
        # Initialize Firebase
        self.firebase = pyrebase.initialize_app(firebase_config)
        # Get a reference to the database service
        self.db = self.firebase.database()
        logger.info("Firebase client initialized successfully")
    
    def get_articles(self, country: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get articles for a specific country directly from Firebase
        
        Args:
            country: The country to get articles for (case insensitive)
            limit: The maximum number of articles to return (default: 10, max: 20)
            
        Returns:
            A list of articles, sorted by date (newest first)
        """
        # Ensure limit doesn't exceed maximum
        if limit > 20:
            logger.warning(f"Requested limit {limit} exceeds maximum of 20, using 20 instead")
            limit = 20
            
        # Convert country to lowercase for consistency
        country = country.lower()
        logger.info(f"Retrieving up to {limit} articles for country: {country}")
        
        try:
            # First try to use the article index for efficiency
            articles = self.get_articles_from_index(country, limit)
            if articles:
                return articles
                
            # If no index or no articles found, fall back to direct retrieval
            logger.info(f"No articles found in index for {country}, trying direct retrieval")
            return self.get_articles_direct(country, limit)
            
        except Exception as e:
            logger.error(f"Error retrieving articles for country {country}: {e}")
            return []
    
    def get_articles_from_index(self, country: str, limit: int) -> List[Dict[str, Any]]:
        """
        Get articles using the pre-computed article index
        
        Args:
            country: The country to get articles for (lowercase)
            limit: The maximum number of articles to return
            
        Returns:
            A list of articles, or empty list if no index exists
        """
        try:
            # Get the latest article IDs from the index
            latest_ids_ref = self.db.child("articleIndex").child(country).child("latestArticles")
            latest_ids = latest_ids_ref.get().val() or []
            
            if not latest_ids:
                logger.info(f"No article index found for country: {country}")
                return []
            
            # Limit to requested number
            latest_ids = latest_ids[:limit]
            logger.info(f"Found {len(latest_ids)} article IDs in index for {country}")
            
            # Get the actual articles
            articles = []
            for article_id in latest_ids:
                article_ref = self.db.child("articles").child(country).child(article_id)
                article_data = article_ref.get().val()
                if article_data:
                    # Add the ID to the article data
                    article_data["id"] = article_id
                    articles.append(article_data)
                else:
                    logger.warning(f"Article {article_id} referenced in index but not found in database")
            
            logger.info(f"Retrieved {len(articles)} articles for {country} using article index")
            return articles
            
        except Exception as e:
            logger.error(f"Error getting articles from index for country {country}: {e}")
            return []
    
    def get_articles_direct(self, country: str, limit: int) -> List[Dict[str, Any]]:
        """
        Get articles directly from the articles collection
        
        Args:
            country: The country to get articles for (lowercase)
            limit: The maximum number of articles to return
            
        Returns:
            A list of articles, sorted by date (newest first)
        """
        try:
            # Get all articles for the country
            articles_ref = self.db.child("articles").child(country)
            articles_data = articles_ref.get().val() or {}
            
            if not articles_data:
                logger.info(f"No articles found for country: {country}")
                return []
            
            # Process the data structure to extract articles
            all_articles = []
            
            # Iterate through article IDs
            for article_id, article_data in articles_data.items():
                if not isinstance(article_data, dict):
                    continue
                    
                # Add the ID to the article data
                article_data["id"] = article_id
                all_articles.append(article_data)
            
            # Sort articles by date (newest first)
            # Using the datePublishedUnix field from metadata for accurate sorting
            all_articles.sort(
                key=lambda x: int(x.get("metadata", {}).get("datePublishedUnix", 0) or 0), 
                reverse=True
            )
            
            # Log the number of articles found
            logger.info(f"Found {len(all_articles)} articles for {country} via direct retrieval")
            
            # Return only the requested number of articles
            return all_articles[:limit]
            
        except Exception as e:
            logger.error(f"Error getting articles directly for country {country}: {e}")
            return []
