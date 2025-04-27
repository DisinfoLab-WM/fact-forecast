import os
import pyrebase
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get Firebase configuration from environment variables
firebase_config = {
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    # For an open database with no authentication, we might not need these
    # but they're typically part of the config
    "apiKey": os.getenv("FIREBASE_API_KEY", ""),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "")
}

def print_database():
    """Connect to Firebase and print the entire database contents"""
    try:
        # Initialize Firebase app
        firebase = pyrebase.initialize_app(firebase_config)
        
        # Get a reference to the database
        db = firebase.database()
        
        print("Successfully connected to Firebase database")
        print(f"Database URL: {firebase_config['databaseURL']}")
        
        # Attempt to get all data
        print("\nAttempting to retrieve all data...")
        all_data = db.get()
        
        # Check if we got any data
        if all_data.val() is None:
            print("No data found in the database")
            return
        
        # Print the data in a readable format
        print("\nDatabase contents:")
        print(json.dumps(all_data.val(), indent=2))
        
        # Print some statistics about the data
        if isinstance(all_data.val(), dict):
            top_level_keys = list(all_data.val().keys())
            print(f"\nFound {len(top_level_keys)} top-level collections: {', '.join(top_level_keys)}")
            
            # If there's an 'articles' collection, show some stats about it
            if 'articles' in all_data.val():
                articles = all_data.val()['articles']
                if isinstance(articles, dict):
                    countries = list(articles.keys())
                    print(f"\nArticles collection contains data for {len(countries)} countries: {', '.join(countries)}")
                    
                    # Show a sample of articles from the first country if available
                    if countries:
                        first_country = countries[0]
                        country_data = articles[first_country]
                        if isinstance(country_data, dict):
                            dates = list(country_data.keys())
                            article_count = sum(len(date_data) for date_data in country_data.values() if isinstance(date_data, dict))
                            print(f"\nSample from {first_country}: {len(dates)} dates, {article_count} total articles")
        
    except Exception as e:
        print(f"Error connecting to Firebase: {e}")

if __name__ == "__main__":
    print_database()
