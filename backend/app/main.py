from fastapi import FastAPI, HTTPException, Query, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional, Set
import os
import uvicorn
import logging
from pydantic import BaseModel

from app.firebase_client import FirebaseClient

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

# Initialize FastAPI app
app = FastAPI(
    title="_map_backend",
    description="API for accessing articles from a Firebase Realtime Database",
    version="0.2.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Firebase client
firebase_client = FirebaseClient()

@app.get("/")
async def root():
    """Root endpoint to check if the API is running"""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the _map_backend API"}

@app.get("/articles/{country}")
async def get_articles(
    country: str,
    limit: int = Query(default=10, ge=1, le=20, description="Maximum number of articles to return (max: 20)")
):
    """
    Get articles for a specific country directly from Firebase
    
    Parameters:
    - country: The country code (e.g., 'usa')
    - limit: Maximum number of articles to return (default: 10, max: 20)
    
    Returns:
    - A list of articles for the specified country
    """
    try:
        # Convert country to lowercase to match database structure
        country = country.lower()
        
        # Log the request
        logger.info(f"GET /articles/{country} - Request received with parameters: limit={limit}")
        
        # Get articles directly from Firebase
        articles = firebase_client.get_articles(country, limit)
        
        # Log the response
        logger.info(f"GET /articles/{country} - Retrieved {len(articles)} articles from Firebase")
        
        return articles
    except Exception as e:
        logger.error(f"Error getting articles for {country}: {e}")
        raise HTTPException(status_code=500, detail=str(e))







if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
