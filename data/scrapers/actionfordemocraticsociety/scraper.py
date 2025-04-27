import feedparser
import json
import time
import re

# Faktograf RSS Feed URL
rss_url = "https://hibrid.info/category/fact-checking/feed/"

feed = feedparser.parse(rss_url)

articles = {"articles": {}}

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

for index, entry in enumerate(feed.entries):
    full_text = entry.content[0].value if 'content' in entry else entry.description
    full_text = remove_html_tags(full_text)

    articles["articles"][str(index)] = {
        "title": entry.title,
        "text": full_text.strip(),
        "author": entry.get("author", ""),
        "date_published": entry.published,
        "unix_date_published": time.mktime(entry.published_parsed) if entry.published_parsed else None,
        "organization_country": "kosovo",  # Assuming the organization is based in Kosovo
        "site_name": "actionfordemocraticsociety", # Assuming the site name is actionfordemocraticsociety
        "url": entry.link,
        "language": "sq",  # Assuming Albanian for all articles
    }

# Save articles to a local JSON file
with open("data.json", "w", encoding='utf-8') as json_file:
    json.dump(articles, json_file, indent=4, ensure_ascii=False)

print("Success")