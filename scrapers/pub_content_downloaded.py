import json
import os
from google.cloud import pubsub_v1

from models.downloaded_article import DownloadedArticle

publisher = pubsub_v1.PublisherClient()

def publish(downloaded_article: DownloadedArticle):
  topic_name = 'projects/{project_id}/topics/{topic}'.format(
      project_id='hedgehog-c9b07',
      topic='content_downloaded',  # Set this to something appropriate.
  )
  # publisher.create_topic(name=topic_name)
  future = publisher.publish(topic_name, bytes(json.dumps(downloaded_article.__dict__), encoding='utf8') , spam='eggs')
  future.result()
