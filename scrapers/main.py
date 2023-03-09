import json
import os
from google.cloud import pubsub_v1
from models.downloaded_article import DownloadedArticle
from pub_content_downloaded import publish

from scrapers.cnbc.cnbc import scrape_with_scrapy

topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id="hedgehog-c9b07",
    topic='new_ticker_added',  # Set this to something appropriate.
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id="hedgehog-c9b07",
    sub='new_ticker_added-sub',  # Set this to something appropriate.
)

def callback(message):
    data = json.loads(message.data.decode())
    content = scrape_with_scrapy(data['stock'])
    articles = json.loads(content)

    for article in articles:
        publish(downloaded_article=DownloadedArticle(
            data['stock'],
            article['url'],
            article['title'],
            article['pub_time'],
            article['update_time'],
            article['content'],

        ))
    message.ack()

with pubsub_v1.SubscriberClient() as subscriber:
    # subscriber.create_subscription(
    #     name=subscription_name, topic=topic_name)
    future = subscriber.subscribe(subscription_name, callback)
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()