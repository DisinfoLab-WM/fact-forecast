# Fact-Forecast Data Processing System

This directory contains the data processing system for the Fact-Forecast application. The system is designed to collect fact-checking articles from various sources around the world, process them into a standardized format, and store them in a Firebase Realtime Database for use by the Fact-Forecast application.

## System Overview

The data processing system consists of:

1. **Scrapers**: Individual scripts that collect articles from specific fact-checking sources
2. **Processing Script**: A central script that runs the scrapers and processes their output
3. **Firebase Integration**: Logic to store processed articles in the Firebase database
4. **Duplicate Prevention**: Mechanisms to prevent duplicate articles and track the latest articles from each source

## How to Run

```bash
python process_scrapers.py
```

This will run all scrapers defined in the `SCRAPER_COUNTRY_MAPPING` dictionary and process their output.

## Adding a New Scraper

### 1. Create a New Scraper Directory

Create a new directory under `scrapers/` with the name of your scraper (use lowercase):

```bash
mkdir -p scrapers/your_scraper_name
```

### 2. Create the Scraper Script

Create a `scraper.py` file in your scraper directory. The script should:

- Collect articles from your target source
- Format them according to the standard format (see below)
- Save them to a `data.json` file in the same directory

### 3. Standard Article Format

Your scraper should output a `data.json` file with the following structure:

```json
{
  "articles": {
    "0": {
      "title": "Article Title",
      "text": "Full article text...",
      "author": "Author Name",
      "date_published": "Publication date in any format",
      "unix_date_published": 1729372800,  // Unix timestamp (seconds since epoch)
      "organization_country": "Country Name",
      "site_name": "Source Name",
      "url": "https://source.com/article",
      "language": "en"  // ISO language code
    },
    "1": {
      // Another article
    }
  }
}
```

### 4. Add to Country Mapping

Add your scraper to the `SCRAPER_COUNTRY_MAPPING` dictionary in `process_scrapers.py`:

```python
SCRAPER_COUNTRY_MAPPING = {
    "ocote": "guatemala",
    "greecefactcheck": "greece",
    "your_scraper_name": "target_country"  # Add your scraper here
}
```

## How Duplicate Prevention Works

The system uses a smart tracking mechanism to prevent duplicate articles and minimize database reads:

1. **Source Tracking**: For each source and country combination, the system tracks the most recent article's ID and timestamp in the `sourceTracking` node of the database.

2. **Incremental Processing**: When processing new articles from a scraper:
   - Articles are sorted by publication timestamp
   - Any article with a timestamp older than or equal to the latest tracked article is skipped
   - Only newer articles are added to the database

3. **Unique Article IDs**: Each article gets a unique ID generated from its title, URL, and source using an MD5 hash, ensuring that even if the same article is processed twice, it will have the same ID.

## Database Structure

The system uses the following Firebase database structure:

```
/articles
  /country_name (lowercase)
    /article_uuid
      /metadata
        title: "Article Title"
        source: "source_name"
        datePublished: "YYYY-MM-DD"
        datePublishedUnix: 1729372800
        dateAdded: "YYYY-MM-DD"
        dateAddedUnix: 1729459200
        url: "https://source.com/article"
        language: "en"
        author: "Author Name"
      /content
        articleText: "Full article text..."
        categories: []
        hyperLinks: ["https://..."] 
        issues: []
        locations: ["Country"]
        people: []
      /factCheck
        determination: ""
        explanation: ""
      /media
        caption: ""
        imageUrl: ""

/sourceTracking
  /country_name (lowercase)
    /source_name (lowercase)
      latestArticleId: "article_uuid"
      latestPublishedDate: "YYYY-MM-DD"
      latestPublishedUnix: 1729372800
```

## Environment Configuration

The system requires a `.env` file with the following variables:

```
# Firebase configuration
FIREBASE_DATABASE_URL=https://your-database-url.firebaseio.com
FIREBASE_API_KEY=
FIREBASE_AUTH_DOMAIN=
FIREBASE_STORAGE_BUCKET=
```

For an open Firebase database, only the `FIREBASE_DATABASE_URL` is required.

## Logs

Logs are stored in the `logs/` directory. The main log file is `scraper_process.log`, which contains information about the scraper runs, article processing, and any errors that occur.

## Troubleshooting

### Scraper Not Running

- Check that your scraper is in the `SCRAPER_COUNTRY_MAPPING` dictionary
- Verify that your scraper directory contains a `scraper.py` file
- Check the logs for any errors

### No Articles Being Added

- Check that your scraper is producing a valid `data.json` file
- Verify that the articles have `unix_date_published` timestamps
- Check if the articles are newer than the latest tracked article
- Look for errors in the logs

### Firebase Connection Issues

- Verify your `.env` file contains the correct Firebase URL
- Check if your Firebase database is accessible
- Ensure you have the necessary permissions