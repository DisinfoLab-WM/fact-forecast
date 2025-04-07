from fastapi import FastAPI, HTTPException, Query, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional, Set
import os
import uvicorn
import logging
from pydantic import BaseModel

from app.firebase_client import FirebaseClient
from app.cache import ArticleCache

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler(os.path.join(logs_dir, "app.log"), mode='a'),  # Log to file
    ]
)
logger = logging.getLogger(__name__)

# Define models for request/response
class RefreshCacheRequest(BaseModel):
    countries: List[str]

# Initialize FastAPI app
app = FastAPI(
    title="_map_backend",
    description="API for accessing articles from a Firebase Realtime Database with caching",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define cache file path
CACHE_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "article_cache.json")

# Create data directory if it doesn't exist
os.makedirs(os.path.dirname(CACHE_FILE_PATH), exist_ok=True)

# Initialize Firebase client and cache
firebase_client = FirebaseClient()
article_cache = ArticleCache(CACHE_FILE_PATH)

# Set default whitelisted countries if not already set
if not article_cache.get_whitelisted_countries():
    default_countries = ["USA", "UK", "CANADA", "AUSTRALIA", "INDIA"]
    article_cache.set_whitelisted_countries(default_countries)

@app.get("/")
async def root():
    """Root endpoint to check if the API is running"""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the _map_backend API"}

@app.get("/articles/{country}")
async def get_recent_articles(
    country: str,
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of articles to return")
):
    """
    Get the most recent articles for a specific country
    
    Parameters:
    - country: The country code (e.g., 'USA')
    - limit: Maximum number of articles to return (default: 10, min: 1, max: 100)
    
    Returns:
    - A list of the most recent articles for the specified country
    """
    try:
        # Convert country to uppercase to ensure consistent formatting
        country = country.upper()
        
        # Log all query parameters
        logger.info(f"GET /articles/{country} - Request received with parameters: limit={limit}")
        
        # If limit is greater than 10, always use Firebase directly
        if limit > 10:
            logger.info(f"GET /articles/{country} - Limit > 10, bypassing cache and fetching directly from Firebase")
            articles = firebase_client.get_recent_articles_by_country(country, limit)
            logger.info(f"GET /articles/{country} - Retrieved {len(articles)} articles from Firebase")
            source = "firebase"
        else:
            # Check if country is in cache
            cached_articles = article_cache.get_articles(country)
            
            if cached_articles is not None:
                logger.info(f"GET /articles/{country} - Cache HIT - Returning {min(len(cached_articles), limit)} articles from cache")
                # Return the cached articles, limited to the requested number
                articles = cached_articles[:limit]
                source = "cache"
            else:
                logger.info(f"GET /articles/{country} - Cache MISS - Fetching from Firebase")
                # Fetch from Firebase if not in cache
                articles = firebase_client.get_recent_articles_by_country(country, limit)
                logger.info(f"GET /articles/{country} - Retrieved {len(articles)} articles from Firebase")
                source = "firebase"
        
        # Return the articles along with metadata
        response = {
            "country": country,
            "count": len(articles),
            "limit": limit,
            "source": source,
            "articles": articles
        }
        
        logger.info(f"GET /articles/{country} - Returning {len(articles)} articles from {source}")
        return response
    except Exception as e:
        logger.error(f"Error getting articles for {country}: {e}")
        # Handle errors
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refresh-cache")
async def refresh_cache(request: RefreshCacheRequest):
    """
    Refresh the cache for specified countries
    
    This endpoint should be called:
    - Every 12 hours by a scheduled task
    - Manually after updating the Firebase database
    
    Only whitelisted countries will be cached.
    """
    try:
        logger.info(f"POST /refresh-cache - Request received for countries: {request.countries}")
        
        # Log statistics about the request
        whitelisted = article_cache.get_whitelisted_countries()
        requested_count = len(request.countries)
        whitelisted_count = len(whitelisted)
        
        # Count countries in request that are not in whitelist
        non_whitelisted = [c.upper() for c in request.countries if c.upper() not in set(whitelisted)]
        
        logger.info(f"POST /refresh-cache - Request includes {len(non_whitelisted)} non-whitelisted countries: {non_whitelisted}")
        
        # Filter to only include whitelisted countries
        countries_to_refresh = []
        for country in request.countries:
            country = country.upper()
            if article_cache.is_country_whitelisted(country):
                countries_to_refresh.append(country)
                logger.info(f"POST /refresh-cache - Country {country} is whitelisted and will be refreshed")
            else:
                logger.warning(f"POST /refresh-cache - Country {country} is not whitelisted and will not be cached")
                
        logger.info(f"POST /refresh-cache - Will refresh {len(countries_to_refresh)}/{requested_count} requested countries")
        
        # Refresh cache for each country
        results = {}
        for country in countries_to_refresh:
            try:
                # Get only 10 articles for the country (to minimize Firebase reads)
                articles = firebase_client.get_recent_articles_by_country(country, limit=10)
                
                # Update cache
                article_cache.set_articles(country, articles)
                
                results[country] = {
                    "status": "success",
                    "article_count": len(articles)
                }
                logger.info(f"Cache refreshed for {country} with {len(articles)} articles")
            except Exception as e:
                results[country] = {
                    "status": "error",
                    "message": str(e)
                }
                logger.error(f"Error refreshing cache for {country}: {e}")
        
        response = {
            "message": "Cache refresh completed",
            "results": results
        }
        
        # Log a summary of the refresh operation
        success_count = sum(1 for country, result in results.items() if result["status"] == "success")
        error_count = sum(1 for country, result in results.items() if result["status"] == "error")
        total_articles = sum(result["article_count"] for country, result in results.items() 
                            if result["status"] == "success" and "article_count" in result)
        
        logger.info(f"POST /refresh-cache - Completed: {success_count} countries successful, {error_count} failed, {total_articles} total articles cached")
        return response
    except Exception as e:
        logger.error(f"Error in refresh cache endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cache-status")
async def get_cache_status():
    """
    Get the current status of the cache
    
    Returns information about cached countries, last refresh times, etc.
    """
    try:
        logger.info("GET /cache-status - Request received")
        status = article_cache.get_cache_status()
        
        # Log detailed information about the cache status
        cached_countries = status.get("cached_countries", [])
        whitelisted_countries = status.get("whitelisted_countries", [])
        
        logger.info(f"GET /cache-status - Cache has {len(cached_countries)} countries cached out of {len(whitelisted_countries)} whitelisted")
        logger.info(f"GET /cache-status - Cached countries: {cached_countries}")
        logger.info(f"GET /cache-status - Whitelisted countries: {whitelisted_countries}")
        
        return status
    except Exception as e:
        logger.error(f"Error getting cache status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/set-whitelisted-countries")
async def set_whitelisted_countries(request: RefreshCacheRequest):
    """
    Set the list of whitelisted countries
    
    Only these countries will be stored in the cache.
    """
    try:
        logger.info(f"POST /set-whitelisted-countries - Request received with countries: {request.countries}")
        
        # Get the current whitelisted countries for logging
        old_whitelist = article_cache.get_whitelisted_countries()
        
        # Update the whitelist
        article_cache.set_whitelisted_countries(request.countries)
        
        # Get the new whitelist
        new_whitelist = article_cache.get_whitelisted_countries()
        
        # Log the changes
        added = [country for country in new_whitelist if country not in old_whitelist]
        removed = [country for country in old_whitelist if country not in new_whitelist]
        
        if added:
            logger.info(f"POST /set-whitelisted-countries - Added countries to whitelist: {added}")
        if removed:
            logger.info(f"POST /set-whitelisted-countries - Removed countries from whitelist: {removed}")
            
        logger.info(f"POST /set-whitelisted-countries - New whitelist set with {len(new_whitelist)} countries: {new_whitelist}")
        
        return {
            "message": "Whitelisted countries updated",
            "whitelisted_countries": new_whitelist,
            "added": added,
            "removed": removed
        }
    except Exception as e:
        logger.error(f"Error setting whitelisted countries: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/all-data")
async def get_all_data():
    """
    Get all data from the database (for debugging purposes)
    
    WARNING: This can be a large amount of data
    """
    try:
        logger.info("GET /all-data - Request received")
        logger.warning("GET /all-data - Retrieving all data from Firebase (potentially large amount of data)")
        
        data = firebase_client.get_all_data()
        
        # Calculate approximate size of the data for logging
        data_size = len(str(data))
        data_size_kb = data_size / 1024
        
        logger.info(f"GET /all-data - Retrieved approximately {data_size_kb:.2f} KB of data from Firebase")
        
        return {
            "message": "All data retrieved",
            "data": data,
            "approximate_size_kb": data_size_kb
        }
    except Exception as e:
        logger.error(f"Error getting all data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/all-articles/{country}")
async def get_all_articles_by_country(country: str):
    """
    Get all articles for a specific country (for debugging purposes)
    
    Parameters:
    - country: The country code (e.g., 'USA')
    """
    try:
        country = country.upper()
        logger.info(f"GET /all-articles/{country} - Request received")
        
        articles = firebase_client.get_articles_by_country(country)
        
        # Count the number of dates and articles
        if isinstance(articles, dict):
            date_count = len(articles)
            article_count = sum(len(articles_by_date) for date_str, articles_by_date in articles.items() 
                               if isinstance(articles_by_date, dict))
            logger.info(f"GET /all-articles/{country} - Retrieved articles for {date_count} dates, total of {article_count} articles")
        else:
            logger.info(f"GET /all-articles/{country} - Retrieved data structure is not a dictionary, may be empty or malformed")
        
        return {
            "country": country,
            "articles": articles
        }
    except Exception as e:
        logger.error(f"Error getting all articles for {country}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
