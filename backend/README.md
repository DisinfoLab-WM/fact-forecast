# Fact-Forecast Backend

A FastAPI backend that connects to a Firebase Realtime Database to serve fact-checking article data with an intelligent caching system to minimize database reads.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── cache.py           # Caching system implementation
│   ├── firebase_client.py  # Firebase connection and data retrieval
│   └── main.py            # FastAPI application and routes
├── data/                  # Cache storage directory
│   └── article_cache.json # Persistent cache file
├── logs/                  # Application logs
│   └── app.log            # Log file
├── .env                   # Environment variables (not tracked by git)
├── .gitignore             # Git ignore file
├── main.py                # Entry point for running the application
└── requirements.txt       # Project dependencies
```

## Features

- **Firebase Integration**: Connects to Firebase Realtime Database to fetch article data
- **Intelligent Caching**: Implements a sophisticated caching system to minimize Firebase reads
- **Environment Variables**: Uses .env file for secure configuration management
- **Comprehensive Logging**: Detailed logging of all operations for debugging and monitoring
- **Auto-generated API Documentation**: Interactive API documentation with Swagger UI and ReDoc
- **Type Validation**: Strong type validation for all API parameters
- **Error Handling**: Robust error handling with appropriate HTTP status codes

## Caching Strategy

The backend implements a sophisticated caching strategy to optimize Firebase usage:

1. **Limited Cache Size**: Cache is limited to 10 most recent articles per country to keep memory usage low
2. **Whitelisted Countries**: Only specific countries are cached (default: USA, UK, CANADA, AUSTRALIA, INDIA)
3. **Cache Bypass**: Requests with limit > 10 bypass the cache completely and go directly to Firebase
4. **Fallback Mechanism**: Non-whitelisted countries always fetch from Firebase without caching
5. **Persistence**: Cache is stored both in memory and as a .json file for persistence across server restarts
6. **Refresh Mechanism**: Cache can be refreshed via API endpoint, ideal for scheduled tasks

## Setup

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_DATABASE_URL=https://your_project.firebaseio.com
FIREBASE_STORAGE_BUCKET=your_project.firebasestorage.app
```

### Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

To run the application:

```
python main.py
```

This will start the server at http://localhost:8000

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:
- http://localhost:8000/docs (Swagger UI) - Interactive documentation with try-it-out functionality
- http://localhost:8000/redoc (ReDoc) - Alternative documentation view

## API Endpoints

### Main Endpoints

#### GET /

Root endpoint to check if the API is running.

#### GET /articles/{country}

Get the most recent articles for a specific country.

**Parameters:**
- `country`: The country code (e.g., 'USA')
- `limit`: Maximum number of articles to return (default: 10, min: 1, max: 100)

**Response:**
```json
{
  "country": "USA",
  "count": 5,
  "limit": 5,
  "source": "cache",  // or "firebase"
  "articles": [...]
}
```

#### POST /refresh-cache

Refresh the cache for specified countries. Only whitelisted countries will be cached.

**Request Body:**
```json
{
  "countries": ["USA", "UK", "CANADA"]
}
```

**Response:**
```json
{
  "message": "Cache refresh completed",
  "results": {
    "USA": { "status": "success", "article_count": 10 },
    "UK": { "status": "success", "article_count": 10 }
  }
}
```

#### GET /cache-status

Get the current status of the cache.

**Response:**
```json
{
  "cached_countries": ["USA", "UK"],
  "whitelisted_countries": ["USA", "UK", "CANADA", "AUSTRALIA", "INDIA"],
  "total_articles": 20,
  "articles_per_country": { "USA": 10, "UK": 10 },
  "cache_coverage": "2/5",
  "last_refresh_time": { ... }
}
```

#### POST /set-whitelisted-countries

Set the list of whitelisted countries that will be stored in the cache.

**Request Body:**
```json
{
  "countries": ["USA", "UK", "CANADA", "AUSTRALIA", "INDIA"]
}
```

### Debug Endpoints

These endpoints are for debugging purposes only and should not be used in production:

#### GET /all-data

Get all data from the database. WARNING: This can be a large amount of data.

#### GET /all-articles/{country}

Get all articles for a specific country without processing or limiting.

## Performance Considerations

- Article data is approximately 20KB each
- Firebase free tier allows ~10GB/month (~52,000 clicks assuming ~200KB/click)
- The caching system significantly reduces Firebase reads
- Cache refresh should be scheduled every 12 hours or after updating Firebase

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request (invalid parameters)
- 404: Not Found
- 500: Internal Server Error

Detailed error messages are provided in the response body and logged to the application logs.
