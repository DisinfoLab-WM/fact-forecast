import feedparser
import json
import time
import re  # Importing regex for HTML parsing

# Faktograf RSS Feed URL
rss_url = "https://www.factchecker.gr/category/fact-check/feed/"

# Parse RSS Feed
feed = feedparser.parse(rss_url)

# Initialize the articles dictionary
articles = {"articles": {}}

# Function to remove HTML tags from text
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# Loop through RSS entries and store in the dictionary
for index, entry in enumerate(feed.entries):
    # Extract full text from content or description
    full_text = entry.content[0].value if 'content' in entry else entry.description
    full_text = remove_html_tags(full_text)  # Clean HTML tags

    articles["articles"][str(index)] = {
        "title": entry.title,
        "text": full_text.strip(),  # Use full text if available and strip whitespace
        "author": entry.get("author", ""),  # Use 'Unknown' if creator is not available
        "date_published": entry.published,
        "unix_date_published": time.mktime(entry.published_parsed) if entry.published_parsed else None,
        "organization_country": "greece",  # Assuming the organization is based in Croatia
        "site_name": "greecefactcheck",
        "url": entry.link,
        "language": "el",  # Assuming Greek for all articles
    }

# Save articles to a local JSON file
with open("data.json", "w", encoding='utf-8') as json_file:
    json.dump(articles, json_file, indent=4, ensure_ascii=False)

print("Success")