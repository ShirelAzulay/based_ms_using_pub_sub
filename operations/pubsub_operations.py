import logging
from google.api_core.exceptions import GoogleAPIError
from operations.bigquery_operations import insert_row_into_bigquery
import config
from operations.gcs_operations import upload_file_to_gcs  # Import GCS upload function

def subscribe_to_messages(
        subscriber,
        subscription_id,
        publisher,
        response_topic,
        bigquery_client,
        gcs_client=None  # Optional GCS client for file operations
):
    """
    Subscribes to messages from a specified Pub/Sub subscription, processes them, and publishes responses.
    Supports optional GCS storage for additional data persistence.

    :param subscriber: Pub/Sub Subscriber client.
    :param subscription_id: Subscription ID to receive messages.
    :param publisher: Pub/Sub Publisher client.
    :param response_topic: Topic to publish processed messages.
    :param bigquery_client: BigQuery client for data storage.
    :param gcs_client: Optional GCS client for file storage operations.
    """
    subscription_path = subscriber.subscription_path(config.GCP_PROJECT_ID, subscription_id)
    logging.info(f"Listening for messages on {subscription_path}...")

    def callback(message):
        message_data = message.data.decode('utf-8')
        logging.info(f"Received message: {message_data}")

        try:
            # Process message content
            processed_message = f"Processed: {message_data}"

            # Store in BigQuery
            insert_row_into_bigquery(bigquery_client, config.DATASET_NAME, config.TABLE_NAME, processed_message)

            # Optionally, use GCS if gcs_client is provided
            if gcs_client:
                bucket_name = config.GCS_BUCKET_NAME
                file_path = f"processed_messages/{message.message_id}.txt"
                upload_file_to_gcs(gcs_client, bucket_name, processed_message, file_path)
                logging.info(f"Stored message in GCS: gs://{bucket_name}/{file_path}")

            # Publish response to response_topic
            publish_message(publisher, config.GCP_PROJECT_ID, response_topic, processed_message)

            # Acknowledge message
            message.ack()
        except Exception as e:
            logging.error(f"Error in callback processing: {e}")
            message.nack()

    # Subscribe and listen for messages
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        streaming_pull_future.result()


def publish_message(publisher, project_id, topic_name, message_text):
    """
    Publishes a message to a specified Pub/Sub topic.

    :param publisher: Pub/Sub Publisher client.
    :param project_id: GCP project ID.
    :param topic_name: The Pub/Sub topic name.
    :param message_text: The message to be published.
    """
    topic_path = publisher.topic_path(project_id, topic_name)
    message_bytes = message_text.encode('utf-8')

    try:
        future = publisher.publish(topic_path, data=message_bytes)
        future.result()  # Ensures message publish is completed
        logging.info(f"Published message to topic {topic_name}: {message_text}")
    except GoogleAPIError as e:
        logging.error(f"Failed to publish message to {topic_name}: {e}")
