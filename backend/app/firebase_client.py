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
    
    def get_all_data(self) -> Dict[str, Any]:
        """Get all data from the database"""
        logger.info("Attempting to retrieve all data from Firebase")
        try:
            all_data = self.db.get()
            result = {}
            
            if all_data.each() is not None:
                for data in all_data.each():
                    result[data.key()] = data.val()
                    
            # Log the top-level keys found
            top_level_keys = list(result.keys())
            logger.info(f"Retrieved all data from Firebase with {len(top_level_keys)} top-level keys: {top_level_keys}")
            
            return result
        except Exception as e:
            logger.error(f"Error reading all data from database: {e}")
            raise Exception(f"Error reading from database: {e}")
    
    def get_articles_by_country(self, country: str) -> Dict[str, Any]:
        """Get all articles for a specific country"""
        logger.info(f"Attempting to retrieve all articles for country: {country}")
        try:
            articles = self.db.child("articles").child(country).get()
            if articles.val() is None:
                logger.info(f"No articles found for country: {country}")
                return {}
                
            articles_data = articles.val()
            
            # Count the number of dates and articles for logging
            if isinstance(articles_data, dict):
                date_count = len(articles_data)
                article_count = 0
                for date_str, date_data in articles_data.items():
                    if isinstance(date_data, dict):
                        article_count += len(date_data)
                logger.info(f"Retrieved articles for country {country}: {date_count} dates, {article_count} total articles")
            else:
                logger.warning(f"Unexpected data structure for country {country} articles")
                
            return articles_data
        except Exception as e:
            logger.error(f"Error reading articles for country {country}: {e}")
            raise Exception(f"Error reading articles for country {country}: {e}")
    
    def get_recent_articles_by_country(self, country: str, limit: int) -> List[Dict[str, Any]]:
        """
        Get the most recent articles for a specific country
        
        Args:
            country: The country to get articles for
            limit: The maximum number of articles to return
            
        Returns:
            A list of articles, sorted by date (newest first)
        """
        logger.info(f"Retrieving up to {limit} recent articles for country: {country}")
        try:
            # Get all articles for the country
            country_articles = self.get_articles_by_country(country)
            if not country_articles:
                logger.info(f"No articles found for country: {country}, returning empty list")
                return []
            
            # Process the data structure to extract articles
            all_articles = []
            
            # Iterate through dates
            for date_str, date_data in country_articles.items():
                # Check if date_data is a dictionary before iterating
                if not isinstance(date_data, dict):
                    continue
                    
                # Iterate through articles for this date
                for article_id, article_data in date_data.items():
                    # Make sure we have valid article data
                    if not isinstance(article_data, dict):
                        continue
                        
                    # Create a new article object with the necessary data
                    article = {}
                    
                    # Copy the metadata, content, factCheck, and media if they exist
                    if "metadata" in article_data:
                        article["metadata"] = article_data["metadata"]
                    if "content" in article_data:
                        article["content"] = article_data["content"]
                    if "factCheck" in article_data:
                        article["factCheck"] = article_data["factCheck"]
                    if "media" in article_data:
                        article["media"] = article_data["media"]
                    
                    # Add date and id to the article data
                    article["date"] = date_str
                    article["id"] = article_id
                    
                    all_articles.append(article)
            
            # Sort articles by date (newest first)
            # Using the datePublishedUnix field from metadata for accurate sorting
            all_articles.sort(
                key=lambda x: int(x.get("metadata", {}).get("datePublishedUnix", 0) or 0), 
                reverse=True
            )
            
            # Log the date range of articles found
            if all_articles:
                newest_date = all_articles[0].get("date", "unknown")
                oldest_date = all_articles[-1].get("date", "unknown") if len(all_articles) > 1 else newest_date
                logger.info(f"Found {len(all_articles)} articles for {country}, date range: {newest_date} to {oldest_date}")
                logger.info(f"Returning {min(len(all_articles), limit)} articles for {country}")
            else:
                logger.info(f"No articles found for {country} after processing")
            
            # Return only the requested number of articles
            return all_articles[:limit]
            
        except Exception as e:
            logger.error(f"Error getting recent articles for country {country}: {e}")
            raise Exception(f"Error getting recent articles for country {country}: {e}")
