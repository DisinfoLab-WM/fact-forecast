import json
import os
import time
from typing import Dict, Any, List, Set
from pathlib import Path
import logging

# Configure logging
logger = logging.getLogger(__name__)



class ArticleCache:
    def __init__(self, cache_file_path: str = "article_cache.json"):
        """
        Initialize the article cache
        
        Args:
            cache_file_path: Path to the cache file
        """
        logger.info(f"Initializing ArticleCache with cache file: {cache_file_path}")
        self.cache_file_path = cache_file_path
        self.cache: Dict[str, Any] = {}
        self.last_refresh_time: Dict[str, float] = {}
        self.whitelisted_countries: Set[str] = set()
        
        # Load cache from file if it exists
        self._load_cache()
        logger.info(f"ArticleCache initialized with {len(self.cache)} countries in cache and {len(self.whitelisted_countries)} whitelisted countries")
    
    def _load_cache(self) -> None:
        """Load the cache from the cache file"""
        logger.info(f"Attempting to load cache from {self.cache_file_path}")
        try:
            if os.path.exists(self.cache_file_path):
                logger.info(f"Cache file exists, loading data")
                with open(self.cache_file_path, 'r') as f:
                    cache_data = json.load(f)
                    
                    # Extract cache and metadata
                    self.cache = cache_data.get("articles", {})
                    self.last_refresh_time = cache_data.get("last_refresh_time", {})
                    self.whitelisted_countries = set(cache_data.get("whitelisted_countries", []))
                    
                    # Log detailed information about the loaded cache
                    cached_countries = list(self.cache.keys())
                    whitelisted_countries = list(self.whitelisted_countries)
                    article_counts = {country: len(articles) for country, articles in self.cache.items()}
                    total_articles = sum(len(articles) for articles in self.cache.values())
                    
                    logger.info(f"Cache loaded from {self.cache_file_path}")
                    logger.info(f"Cached countries ({len(cached_countries)}): {cached_countries}")
                    logger.info(f"Whitelisted countries ({len(whitelisted_countries)}): {whitelisted_countries}")
                    logger.info(f"Total articles in cache: {total_articles}")
                    logger.info(f"Articles per country: {article_counts}")
                    
                    # Log refresh times in human-readable format
                    if self.last_refresh_time:
                        refresh_times = {country: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)) 
                                        for country, timestamp in self.last_refresh_time.items()}
                        logger.info(f"Last refresh times: {refresh_times}")
            else:
                logger.info(f"Cache file does not exist at {self.cache_file_path}, initializing empty cache")
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
            # Initialize empty cache if loading fails
            self.cache = {}
            self.last_refresh_time = {}
            logger.warning("Initialized empty cache due to loading error")
    
    def _save_cache(self) -> None:
        """Save the cache to the cache file"""
        logger.info(f"Attempting to save cache to {self.cache_file_path}")
        try:
            # Create directory if it doesn't exist
            cache_dir = os.path.dirname(self.cache_file_path)
            if cache_dir and not os.path.exists(cache_dir):
                logger.info(f"Creating cache directory: {cache_dir}")
                os.makedirs(cache_dir)
                
            # Save cache with metadata
            cache_data = {
                "articles": self.cache,
                "last_refresh_time": self.last_refresh_time,
                "whitelisted_countries": list(self.whitelisted_countries)
            }
            
            # Log detailed information about what's being saved
            cached_countries = list(self.cache.keys())
            whitelisted_countries = list(self.whitelisted_countries)
            total_articles = sum(len(articles) for articles in self.cache.values())
            
            logger.info(f"Saving cache with {len(cached_countries)} countries and {total_articles} total articles")
            logger.info(f"Cached countries: {cached_countries}")
            logger.info(f"Whitelisted countries: {whitelisted_countries}")
            
            # Calculate approximate size of the cache data
            cache_size = len(json.dumps(cache_data))
            cache_size_kb = cache_size / 1024
            logger.info(f"Cache data size: approximately {cache_size_kb:.2f} KB")
            
            with open(self.cache_file_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
            logger.info(f"Cache successfully saved to {self.cache_file_path}")
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
    
    def get_articles(self, country: str) -> List[Dict[str, Any]]:
        """
        Get articles for a country from the cache
        
        Args:
            country: Country code
            
        Returns:
            List of articles or None if not in cache
        """
        country = country.upper()
        logger.info(f"Attempting to get articles for country {country} from cache")
        
        articles = self.cache.get(country, None)
        
        if articles is not None:
            logger.info(f"Cache HIT for country {country}: found {len(articles)} articles")
            
            # Log the date range if articles exist
            if articles:
                # Sort by date for logging purposes
                sorted_articles = sorted(articles, 
                                         key=lambda x: int(x.get("metadata", {}).get("datePublishedUnix", 0) or 0), 
                                         reverse=True)
                newest_date = sorted_articles[0].get("date", "unknown")
                oldest_date = sorted_articles[-1].get("date", "unknown") if len(sorted_articles) > 1 else newest_date
                logger.info(f"Date range for {country}: {newest_date} to {oldest_date}")
        else:
            logger.info(f"Cache MISS for country {country}")
            
        return articles
    
    def set_articles(self, country: str, articles: List[Dict[str, Any]]) -> None:
        """
        Set articles for a country in the cache
        
        Args:
            country: Country code
            articles: List of articles
        """
        country = country.upper()
        logger.info(f"Attempting to set articles for country {country} in cache")
        
        if country in self.whitelisted_countries:
            # Sort articles by date (newest first)
            sorted_articles = sorted(articles, 
                                     key=lambda x: int(x.get("metadata", {}).get("datePublishedUnix", 0) or 0), 
                                     reverse=True)
            
            # Use all articles passed from main.py (which are already limited)
            articles_to_cache = sorted_articles
            
            # Log information about the articles being cached
            if articles_to_cache:
                newest_date = articles_to_cache[0].get("date", "unknown")
                oldest_date = articles_to_cache[-1].get("date", "unknown") if len(articles_to_cache) > 1 else newest_date
                logger.info(f"Caching {len(articles_to_cache)} articles for {country} with date range: {newest_date} to {oldest_date}")
            else:
                logger.warning(f"No articles to cache for country {country}")
            
            # Update the cache
            self.cache[country] = articles_to_cache
            self.last_refresh_time[country] = time.time()
            
            # Log the update time in human-readable format
            refresh_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.last_refresh_time[country]))
            logger.info(f"Cache updated for country {country} at {refresh_time_str} with {len(articles_to_cache)} articles")
            
            # Save the cache to disk
            self._save_cache()
        else:
            logger.warning(f"Country {country} is not whitelisted, skipping cache update")
    
    def set_whitelisted_countries(self, countries: List[str]) -> None:
        """
        Set the list of whitelisted countries
        
        Args:
            countries: List of country codes
        """
        logger.info(f"Updating whitelisted countries: {countries}")
        
        # Get the current whitelist for comparison
        old_whitelist = self.whitelisted_countries.copy()
        
        # Update the whitelist
        self.whitelisted_countries = {country.upper() for country in countries}
        
        # Identify added and removed countries
        added = [country for country in self.whitelisted_countries if country not in old_whitelist]
        removed = [country for country in old_whitelist if country not in self.whitelisted_countries]
        
        if added:
            logger.info(f"Added countries to whitelist: {added}")
        if removed:
            logger.info(f"Removed countries from whitelist: {removed}")
            # Remove non-whitelisted countries from cache
            for country in removed:
                if country in self.cache:
                    logger.info(f"Removing {country} from cache as it is no longer whitelisted")
                    del self.cache[country]
                    if country in self.last_refresh_time:
                        del self.last_refresh_time[country]
        
        logger.info(f"Whitelisted countries updated to: {list(self.whitelisted_countries)}")
        self._save_cache()
    
    def get_whitelisted_countries(self) -> List[str]:
        """
        Get the list of whitelisted countries
        
        Returns:
            List of country codes
        """
        countries = list(self.whitelisted_countries)
        logger.info(f"Retrieved {len(countries)} whitelisted countries: {countries}")
        return countries
    
    def is_country_whitelisted(self, country: str) -> bool:
        """
        Check if a country is whitelisted
        
        Args:
            country: Country code
            
        Returns:
            True if the country is whitelisted, False otherwise
        """
        country = country.upper()
        is_whitelisted = country in self.whitelisted_countries
        logger.info(f"Checking if country {country} is whitelisted: {is_whitelisted}")
        return is_whitelisted
    
    def get_cache_status(self) -> Dict[str, Any]:
        """
        Get the status of the cache
        
        Returns:
            Dictionary with cache status information
        """
        logger.info("Retrieving cache status")
        
        # Get basic status information
        cached_countries = list(self.cache.keys())
        whitelisted_countries = list(self.whitelisted_countries)
        
        # Calculate additional statistics
        total_articles = sum(len(articles) for articles in self.cache.values())
        articles_per_country = {country: len(articles) for country, articles in self.cache.items()}
        cache_coverage = f"{len(cached_countries)}/{len(whitelisted_countries)}" if whitelisted_countries else "0/0"
        
        # Create the status object
        status = {
            "cached_countries": cached_countries,
            "whitelisted_countries": whitelisted_countries,
            "total_articles": total_articles,
            "articles_per_country": articles_per_country,
            "cache_coverage": cache_coverage,
            "last_refresh_time": {}
        }
        
        # Convert timestamps to human-readable format
        for country, timestamp in self.last_refresh_time.items():
            status["last_refresh_time"][country] = {
                "timestamp": timestamp,
                "formatted": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
            }
        
        logger.info(f"Cache status: {len(cached_countries)}/{len(whitelisted_countries)} countries cached, {total_articles} total articles")
        logger.info(f"Articles per country: {articles_per_country}")
            
        return status
    
    def clear_cache(self) -> None:
        """Clear the entire cache"""
        logger.warning("Clearing entire cache")
        
        # Log what's being cleared
        cached_countries = list(self.cache.keys())
        total_articles = sum(len(articles) for articles in self.cache.values())
        logger.info(f"Clearing cache with {len(cached_countries)} countries and {total_articles} articles")
        logger.info(f"Countries being cleared: {cached_countries}")
        
        # Clear the cache
        self.cache = {}
        self.last_refresh_time = {}
        
        # Save the empty cache
        self._save_cache()
        logger.info("Cache has been cleared successfully")
