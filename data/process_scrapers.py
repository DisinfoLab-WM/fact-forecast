import os
import json
import time
import hashlib
import subprocess
import pyrebase
from dotenv import load_dotenv
from datetime import datetime
import logging
import uuid

# Configure logging
# Ensure logs directory exists
logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(logs_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(logs_dir, 'scraper_process.log'))
    ]
)
logger = logging.getLogger('process_scrapers')

# Load environment variables
load_dotenv()

# Firebase configuration
firebase_config = {
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "apiKey": os.getenv("FIREBASE_API_KEY", ""),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "")
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Constants
SCRAPERS_DIR = os.path.join(os.path.dirname(__file__), 'scrapers')
MAX_WAIT_TIME = 300  # Maximum time to wait for scraper to complete (in seconds)

# Country mapping for scrapers
SCRAPER_COUNTRY_MAPPING = {
    "ocote": "guatemala",         # Ocote is from Guatemala
    "greecefactcheck": "greece",  # Greek fact-checking organization
    "actionfordemocraticsociety": "kosovo",
    "boom": "india",
    "cablecheck": "nigeria",
    "cotejoinfo": "venezuela",
    "digiteye": "india",
    "annielab": "hongkong",
    "cazadoresdefakenews": "venezuela",
    "checkyourfact": "united states",
    "demagogassociation": "poland",
    "ecuadorchequea": "ecuador",
    "efectochequea": "ecuador",
    "ellinikahoaxes": "greece"
}

def generate_article_id(title, url, source):
    """Generate a unique ID for an article based on its title, URL, and source"""
    # Create a string combining title, url, and source
    combined = f"{title}|{url}|{source}"
    # Generate a hash
    hash_obj = hashlib.md5(combined.encode())
    # Return a UUID-like string
    return str(uuid.UUID(hash_obj.hexdigest()))

def get_latest_article_for_source(country, source):
    """Get the latest article ID and timestamp for a specific source and country"""
    # Ensure country and source are lowercase
    country = country.lower()
    source = source.lower()
    
    try:
        source_tracking = db.child("sourceTracking").child(country).child(source).get().val()
        if source_tracking:
            return {
                "latestArticleId": source_tracking.get("latestArticleId"),
                "latestPublishedUnix": source_tracking.get("latestPublishedUnix", 0)
            }
        return None
    except Exception as e:
        logger.error(f"Error getting latest article for {country}/{source}: {e}")
        return None

def update_latest_article(country, source, article, article_id):
    """Update the latest article tracker for a source and country"""
    # Ensure country and source are lowercase
    country = country.lower()
    source = source.lower()
    
    try:
        db.child("sourceTracking").child(country).child(source).set({
            "latestArticleId": article_id,
            "latestPublishedDate": article.get("metadata", {}).get("datePublished", ""),
            "latestPublishedUnix": article.get("metadata", {}).get("datePublishedUnix", 0)
        })
        logger.info(f"Updated latest article for {country}/{source}: {article_id}")
    except Exception as e:
        logger.error(f"Error updating latest article for {country}/{source}: {e}")

def run_scraper(scraper_name):
    """Run a specific scraper and wait for it to complete"""
    scraper_path = os.path.join(SCRAPERS_DIR, scraper_name, 'scraper.py')
    data_path = os.path.join(SCRAPERS_DIR, scraper_name, 'data.json')
    
    # Check if scraper exists
    if not os.path.exists(scraper_path):
        logger.error(f"Scraper not found: {scraper_path}")
        return None
    
    # Remove any existing data file
    if os.path.exists(data_path):
        os.remove(data_path)
    
    # Run the scraper
    logger.info(f"Running scraper: {scraper_name}")
    process = subprocess.Popen(['python', scraper_path], cwd=os.path.join(SCRAPERS_DIR, scraper_name))
    
    # Wait for data file to be created
    wait_time = 0
    while not os.path.exists(data_path) and wait_time < MAX_WAIT_TIME:
        time.sleep(1)
        wait_time += 1
    
    if not os.path.exists(data_path):
        logger.error(f"Scraper timed out: {scraper_name}")
        return None
    
    # Wait a bit more to ensure the file is fully written
    time.sleep(2)
    
    # Load the data
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded data from {scraper_name}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {scraper_name}: {e}")
        return None

def transform_standard_article(article_data, source):
    """Transform article data from any scraper to our standardized format"""
    # Ensure source is lowercase
    source = source.lower()
    
    # Extract date in YYYY-MM-DD format from the published date
    # Assuming published date is in a standard format
    date_published = article_data.get("date_published", "")
    date_str = datetime.fromtimestamp(article_data.get("unix_date_published", 0)).strftime('%Y-%m-%d')
    
    # Get organization country and ensure it's lowercase
    org_country = article_data.get("organization_country", "").lower()
    
    # Create the standardized article structure
    transformed = {
        "metadata": {
            "title": article_data.get("title", ""),
            "source": source,
            "datePublished": date_str,
            "datePublishedUnix": article_data.get("unix_date_published", 0),
            "dateAdded": datetime.now().strftime('%Y-%m-%d'),
            "dateAddedUnix": int(time.time()),
            "url": article_data.get("url", ""),
            "language": article_data.get("language", "es").lower(),
            "author": article_data.get("author", "")
        },
        "content": {
            "articleText": article_data.get("text", ""),
            "categories": [],
            "hyperLinks": [article_data.get("url", "")],
            "issues": [],
            "locations": [org_country],
            "people": []
        },
        "factCheck": {
            "determination": "",
            "explanation": ""
        },
        "media": {
            "caption": "",
            "imageUrl": ""
        }
    }
    
    return transformed

def process_standard_data(data, source, force_update=False):
    """Process scraper data and add to Firebase
    
    This function handles data from any scraper that produces output in the standard format:
    {
        "articles": {
            "0": { article data },
            "1": { article data },
            ...
        }
    }
    """
    if not data or 'articles' not in data:
        logger.error(f"No articles found in data from {source}")
        return
    
    # Get country for this source and ensure it's lowercase
    source = source.lower()
    country = SCRAPER_COUNTRY_MAPPING.get(source, "unknown")
    
    # Get articles from the data
    articles_dict = data.get('articles', {})
    
    logger.info(f"Processing {len(articles_dict)} articles for {country} from {source}")
    
    # Get the latest article for this source/country
    latest_article = get_latest_article_for_source(country, source)
    
    # Convert dictionary to list and sort by unix timestamp
    articles = []
    for article_id, article_data in articles_dict.items():
        articles.append(article_data)
    
    # Sort articles by unix timestamp
    articles.sort(key=lambda x: x.get("unix_date_published", 0))
    
    # Process each article
    new_articles = []
    for article_data in articles:
        # Skip if this article is older than our latest (unless force update)
        article_timestamp = article_data.get("unix_date_published", 0)
        if not force_update and latest_article and article_timestamp <= latest_article.get("latestPublishedUnix", 0):
            logger.info(f"Skipping article {article_data.get('title', '')} - older than latest tracked article")
            continue
        
        # Generate a unique ID for this article
        title = article_data.get("title", "")
        url = article_data.get("url", "")
        article_id = generate_article_id(title, url, source)
        
        # Transform to our standardized format
        transformed_article = transform_standard_article(article_data, source)
        
        # Add to our processing list
        new_articles.append((article_id, transformed_article))
    
    # Add all new articles to database
    if new_articles:
        for article_id, article in new_articles:
            try:
                db.child("articles").child(country).child(article_id).set(article)
                logger.info(f"Added article {article_id} to {country}")
            except Exception as e:
                logger.error(f"Error adding article {article_id} to {country}: {e}")
        
        # Update the latest article tracker
        update_latest_article(country, source, new_articles[-1][1], new_articles[-1][0])
        
        logger.info(f"Added {len(new_articles)} new articles for {country} from {source}")
    else:
        logger.info(f"No new articles to add for {country} from {source}")

def main():
    """Main function to run all scrapers and process their data"""
    logger.info("Starting scraper processing")
    
    # Only process scrapers defined in the country mapping dictionary
    scrapers = list(SCRAPER_COUNTRY_MAPPING.keys())
    
    logger.info(f"Processing {len(scrapers)} scrapers: {', '.join(scrapers)}")
    
    # Process each scraper in the mapping
    for scraper in scrapers:
        # Check if the scraper directory exists
        scraper_dir = os.path.join(SCRAPERS_DIR, scraper)
        scraper_script = os.path.join(scraper_dir, 'scraper.py')
        
        if not os.path.exists(scraper_dir) or not os.path.exists(scraper_script):
            logger.warning(f"Scraper directory or script not found for {scraper}. Skipping.")
            continue
        
        # Run the scraper and process its data
        data = run_scraper(scraper)
        if data:
            process_standard_data(data, source=scraper)
    
    logger.info("Completed scraper processing")

if __name__ == "__main__":
    main()
