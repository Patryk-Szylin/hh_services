import asyncio
import json
import os
from google.cloud import pubsub_v1
from google.api_core import retry

from chatgpt import summarise
from firestore import addSummary


topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id="hedgehog-c9b07",
    topic='content_downloaded',  # Set this to something appropriate.
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id="hedgehog-c9b07",
    sub='sub_one',  # Set this to something appropriate.
)

def callback(message):
    data = json.loads(message.data.decode())
    if(data['content'] == None):
      message.ack()
      # Store the failed attempt somehwere
      print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      return
    
    summary = summarise(data['stock_ticker'], data['content'])
    print(data)

    addSummary(data, summary)
    
    message.ack()
      



subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path("hedgehog-c9b07", "sub_one")


# async def asd():
#   # Wrap the subscriber in a 'with' block to automatically call close() to
#   # close the underlying gRPC channel when done.
#   with subscriber:
#       # The subscriber pulls a specific number of messages. The actual
#       # number of messages pulled may be smaller than max_messages.
#       response = subscriber.pull(
#           request={"subscription": subscription_path, "max_messages": 20},
#           retry=retry.Retry(deadline=300),
#       )

#       if len(response.received_messages) == 0:
#           return

#       ack_ids = []
#       for received_message in response.received_messages:
#           # print(f"Received: {received_message.message.data}.")
#           data = json.loads(received_message.message.data.decode())
#           print(data['stock_ticker'])
#           await summarise(data['stock_ticker'], data['content'])
#           ack_ids.append(received_message.ack_id)

#       # Acknowledges the received messages so they will not be sent again.
#       subscriber.acknowledge(
#           request={"subscription": subscription_path, "ack_ids": ack_ids}
#       )

#       print(
#           f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
#       )

# asyncio.run(asd())
# flow_control = pubsub_v1.types.FlowControl(max_messages=1)

async def asd():
  with pubsub_v1.SubscriberClient() as subscriber:
      # subscriber.create_subscription(
      #     name=subscription_name, topic=topic_name)
      future = subscriber.subscribe(subscription_name, callback=callback)
      try:
          future.result(timeout=None)
      except KeyboardInterrupt:
          future.cancel()

asyncio.run(asd())