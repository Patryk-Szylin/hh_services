class DownloadedArticle:
    def __init__(self, stock_ticker, url, title, pub_time, update_time, content):
        self.stock_ticker = stock_ticker
        self.url = url
        self.title = title
        self.pub_time = pub_time
        self.update_time = update_time
        self.content = content