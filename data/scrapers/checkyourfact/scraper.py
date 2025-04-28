import feedparser
import json
import time
import re

rss_url = "https://checkyourfact.com/feed/"

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
        "organization_country": "united states",  # Assuming the organization is based in United States
        "site_name": "checkyourfact", # Assuming the site name is checkyourfact
        "url": entry.link,
        "language": "en",  # Assuming English for all articles
    }

with open("data.json", "w", encoding='utf-8') as json_file:
    json.dump(articles, json_file, indent=4, ensure_ascii=False)

print("Success")