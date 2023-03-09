from scrapy.http import Response
import requests
from bs4 import BeautifulSoup


def handle_errors(field):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"WARNING: There was an error scraping '{field}'\n\t{e}")
                return None
        return wrapper
    return decorator

@handle_errors("title")
def get_title(soup):
    return soup.find("h1").text

@handle_errors("pub_time")
def get_pub_time(soup):
    return soup.find("time", itemprop="datePublished")["datetime"]

@handle_errors("update_time")
def get_update_time(soup):
    res = [time["datetime"] for time in soup.find_all("time")]
    if len(res) < 2:
        raise Exception("UpdateTimeNotFound")
    return res[1]

@handle_errors("content")
def get_content(soup):
    return [p.get_text() for p in soup.select("div.group p")]

def is_live_blog(soup):
    return True if soup.select(".Live.Blog.Article") else False


def parse_article_from_url(article_url, html=None):
    print(f"INFO: Scraping {article_url}")
    if html is None:
        response = requests.get(article_url)
        html = response.text

    soup = BeautifulSoup(html, "lxml")
    if is_live_blog(soup):
      print("INFO: Article was live blog, skipping...")
      return None

    title = get_title(soup)
    pub_time = get_pub_time(soup)
    update_time = get_update_time(soup)
    content = get_content(soup)

    return {
        "url": article_url,
        "title": title,
        "pub_time": pub_time,
        "update_time": update_time,
        "content": " ".join(content).replace(" .", ".").replace(". ", ".\n"),
    }
