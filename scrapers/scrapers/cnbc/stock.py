import scrapy, json

from scrapers.cnbc.article import parse_article_from_url


class StockSpider(scrapy.Spider):
    name = "stock"
    allowed_domains = ["www.cnbc.com"]

    def __init__(self, stock="", **kwargs):
        self.start_urls = [f"https://www.cnbc.com/quotes/{stock}?tab=news"]
        super().__init__(**kwargs)

    @staticmethod
    def is_article_valid(article):
        classification = article["contentClassification"]
        if classification:
            if classification[0] == "premium" or classification[0] == "subscriberAlert":
                return False

        if article["type"] == "cnbcvideo":
            return False

        return True

    def parse(self, response):
        raw_json = (
            response.css("script::text")[-2]
            .get()
            .replace("window.__s_data=", "")
            .split("window.__c_data")[0][0:-2]
        )

        json_data = json.loads(raw_json)["quote"]["news"]["latestNews"]
        # with open("test.json", "w") as jsonfile:
        #    jsonfile.write(json.dumps(json_data))

        urls = [
            article["url"] for article in json_data if self.is_article_valid(article)
        ]

        for article_url in urls:
            yield response.follow(article_url, self.parse_article)

    def parse_article(self, response):
        return parse_article_from_url(response.url, html=response.body)
