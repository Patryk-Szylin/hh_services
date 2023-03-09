import scrapy, json
from scrapyscript import Job, Processor
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request

from scrapers.cnbc.stock import StockSpider

def get_scrapy_settings():
    return {
        "BOT_NAME": "stocks",
        "USER_AGENT": "stocks spider",
        "ROBOTSTXT_OBEY": True,
        "LOG_LEVEL": "ERROR",
    }


def scrape_with_scrapy(stock: str) -> str:
    """
    stock: stock to scrape, name should be as it appears on the url

    return: json string
    """
    print(f"Scraping {stock}...")
    processor = Processor(settings=get_scrapy_settings())

    job = Job(StockSpider, stock=stock)
    result = processor.run(job)
    print("DONE")
    return json.dumps(result, indent=2)