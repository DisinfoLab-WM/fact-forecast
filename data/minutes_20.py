# WANT:
# - Title
# - Text
# - Author
# - date_published
# - unix_date_published
# - organization_country: "France"
# - site_name: "20 Minutes"
# - url
# - language: "fr"
#
# HELPFUL:
# - https://www.20minutes.fr/actus
#

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from requests import get as load_page
from re import findall as findall_re
from datetime import datetime

RSS_URL = "https://www.20minutes.fr/actus"

glorm = "c-card-with-summary__content"

class LinkError(BaseException):
    def __init__(self):
        pass

def recursive_get_text(element) -> str:
    if type(element) != Tag:
        return str(element)
    total = ""
    for sect in element.contents:
        total += recursive_get_text(sect)
    return total

# take a div element
def cleanse_content(content) -> str:
    paragraphs = content.find_all("p")
    text = ""
    for p in paragraphs:
        for sect in p.contents:
            text += recursive_get_text(sect)
        text += "\n"
    return ""

def parse_pub_date(text) -> str:
    # _*_mis à jour le DD/MM/YEAR à hhHmm
    # not worried about checking for valid dates since the site is trusted
    date = findall_re("[0-9]{2}/[0-9]{2}/[0-9]{4}", text)[0]
    time = findall_re("[0-9]{2}h[0-9]{2}", text)[0]

    day = date[0:2]
    month = date[3:5]
    year = date[6:10]
    hour = time[0:2]
    minutes = time[3:5]

    proper_format =  f"{year}-{month}-{day} {hour}:{minutes}:00" # cannot access minutes
    unix_format = datetime.fromisoformat(proper_format).timestamp()
    return (proper_format, unix_format)

def parse_article(url):
    if url[0] == '/' or len(url) <= len("https://maison.20minutes.fr/"):
        raise LinkError

    page = load_page(url)
    soup = BeautifulSoup(page.content, features="html.parser")

    title = soup.find("h1").contents[0]
    raw_content = soup.find("div", class_="c-content")
    text = cleanse_content(raw_content)

    # <address>
    #   <div> profile pic </div>
    #   <div>
    #       <p> Author / Publisher </p>
    #       <p>
    #           <time> Initial publication </time>
    #           <time> Updated </time>
    #       </p>
    #   </div>
    # </address>
    address_bar = soup.find("address")
    (author_el, time_els) = address_bar.find_all("div")[1].find_all("p")
    author = str(author_el.contents[0])
    if len(time_els.contents) > 1:
        (date_published, unix_date_published) = parse_pub_date(time_els.contents[1].contents[0])
    else:
        (date_published, unix_date_published) = parse_pub_date(time_els.contents[0].contents[0])

    article_data = {
        "title": title,
        "text": text,
        "author": author,
        "date_published": date_published,
        "unix_date_published": unix_date_published,
        "organization_country": "France",
        "site_name": "20_minutes",
        "url": url,
        "language": "fr"
    }

    return article_data

def parse():
    page = load_page(RSS_URL)
    soup = BeautifulSoup(page.content, features="html.parser")
    articles = soup.find_all("div", class_="c-card-title")
    non_articles_read = 0
    parsed_data = {}

    for (i, art) in enumerate(articles):
        # <div class="c-card-title">
        #   <h3>
        #       <a href="link_we_want"> title </a>
        #   </h3>
        # </div>
        if i == 20 - non_articles_read: # only load 20 articles
            break
        anchor = art.find("a")
        link = anchor["href"]
        try:
            data = parse_article(link)
            parsed_data[str(i-non_articles_read)] = data
        except LinkError: # read a non-article card
            non_articles_read += 1
            continue
    return {"articles": parsed_data}

if __name__ == '__main__':
    #parse()
    articles = parse()
