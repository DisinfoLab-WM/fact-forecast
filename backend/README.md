# _map_backend

A FastAPI backend that connects to a Firebase Realtime Database to serve article data.

## Project Structure

```
_map_backend/
├── app/
│   ├── __init__.py
│   ├── firebase_client.py  # Firebase connection and data retrieval
│   └── main.py             # FastAPI application and routes
└── main.py                 # Entry point for running the application
```

## Setup

### Required Packages

You'll need to install the following packages:

```
pip install fastapi uvicorn pyrebase4
```

### Running the Application

To run the application:

```
python main.py
```

This will start the server at http://localhost:8000

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Endpoints

### GET /articles/{country}

Get the most recent articles for a specific country.

**Parameters:**
- `country`: The country code (e.g., 'USA')
- `limit`: Maximum number of articles to return (default: 10, min: 1, max: 100)

**Example:**
```
GET /articles/USA?limit=5
```

**Response:**
```json
{
  "country": "USA",
  "count": 5,
  "limit": 5,
  "articles": [...]
}
```
