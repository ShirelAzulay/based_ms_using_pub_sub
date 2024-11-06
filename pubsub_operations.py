import logging
from google.api_core.exceptions import GoogleAPIError
import config
from queries import get_all_satellite_data, get_data_within_polygon, get_data_containing_point, \
    get_data_intersecting_polygon, get_data_containing_polygon


def publish_message(publisher, topic_name, message_text):
    topic_path = publisher.topic_path(config.GCP_PROJECT_ID, topic_name)
    message_bytes = message_text.encode('utf-8')
    try:
        future = publisher.publish(topic_path, data=message_bytes)
        future.result()
        logging.info(f"Published message to topic {topic_name}: {message_text}")
    except GoogleAPIError as e:
        logging.error(f"Failed to publish message to {topic_name}: {e}")


def subscribe_to_messages(subscriber, subscription_id, publisher, response_topic, bigquery_client):
    subscription_path = subscriber.subscription_path(config.GCP_PROJECT_ID, subscription_id)
    logging.info(f"Listening for messages on {subscription_path}...")

    def callback(message):
        logging.info(f"Received request message: {message.data.decode('utf-8')}")
        # Placeholder: Replace with actual logic to determine which query to run based on message
        query = get_all_satellite_data()
        query_job = bigquery_client.query(query)
        results = query_job.result()

        # Publishing each result as a message to the response topic
        for row in results:
            publish_message(publisher, response_topic, str(row))
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
