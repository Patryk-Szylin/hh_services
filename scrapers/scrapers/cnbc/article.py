from scrapy.http import Response
import requests
from bs4 import BeautifulSoup


def parse_article_from_url(article_url, html=None):
    if html is None:
        response = requests.get(article_url)
        html = response.text

    soup = BeautifulSoup(html, "lxml")
    title = soup.find("h1").text
    pub_time, *update_time = [time["datetime"] for time in soup.find_all("time")]
    content = [p.get_text() for p in soup.select("div.group p")]

    return {
        "url": article_url,
        "title": title,
        "pub_time": pub_time,
        "update_time": update_time[0] if update_time else None,
        "content": " ".join(content).replace(" .", ".").replace(". ", ".\n"),
    }
