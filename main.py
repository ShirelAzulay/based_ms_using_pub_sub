import os
import logging
from google.cloud import pubsub_v1
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError


# Set up logging
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging is set up.")


# Load environment variables
def load_environment_variables():
    project_id = os.getenv("GCP_PROJECT_ID")
    subscription_id = os.getenv("PUBSUB_SUBSCRIPTION_ID")
    topic_name_request = os.getenv("PUBSUB_TOPIC_REQUEST")
    topic_name_response = os.getenv("PUBSUB_TOPIC_RESPONSE")
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")
    table_id = os.getenv("BIGQUERY_TABLE_ID")

    if not all([project_id, subscription_id, topic_name_request, topic_name_response, dataset_id, table_id]):
        logging.error("One or more environment variables are missing.")
        raise EnvironmentError("One or more environment variables are missing.")

    logging.info("Environment variables loaded successfully.")
    return project_id, subscription_id, topic_name_request, topic_name_response, dataset_id, table_id


# Initialize Pub/Sub Publisher and Subscriber clients
def initialize_pubsub_clients():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    logging.info("Pub/Sub clients initialized successfully.")
    return publisher, subscriber


# Initialize BigQuery Client
def initialize_bigquery_client():
    bigquery_client = bigquery.Client()
    logging.info("BigQuery client initialized successfully.")
    return bigquery_client


# Process a message with try-except for error handling
def process_message(message_text):
    try:
        # Simulate some processing logic
        logging.info(f"Processing message: {message_text}")
        processed_message = f"Processed: {message_text}"
        return processed_message
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        return None  # Return None if an error occurs


# Publish a message to a Pub/Sub topic (Response topic)
def publish_message(publisher, project_id, topic_name, message_text):
    topic_path = publisher.topic_path(project_id, topic_name)
    message_bytes = message_text.encode('utf-8')

    try:
        future = publisher.publish(topic_path, data=message_bytes)
        future.result()  # Wait for the result of the publish
        logging.info(f"Published message to topic {topic_name}: {message_text}")
    except GoogleAPIError as e:
        logging.error(f"Failed to publish message to {topic_name}: {e}")


# Insert a row into a BigQuery table
def insert_row_into_bigquery(bigquery_client, dataset_id, table_id, message_text):
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)
    rows_to_insert = [{"message": message_text}]

    try:
        errors = bigquery_client.insert_rows_json(table_ref, rows_to_insert)
        if errors:
            logging.error(f"Errors while inserting row into BigQuery: {errors}")
        else:
            logging.info("New row has been added to BigQuery")
    except GoogleAPIError as e:
        logging.error(f"Failed to insert row into BigQuery: {e}")


# Subscribe to Pub/Sub and listen for messages from the request topic
def subscribe_to_messages(subscriber, project_id, subscription_id, publisher, response_topic, bigquery_client,
                          dataset_id, table_id):
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    logging.info(f"Listening for messages on {subscription_path}...")

    def callback(message):
        logging.info(f"Received request message: {message.data.decode('utf-8')}")

        try:
            # Process the message
            processed_message = process_message(message.data.decode('utf-8'))
            if processed_message is None:
                raise Exception("Processing failed, skipping further steps.")

            # Insert the processed message into BigQuery
            insert_row_into_bigquery(bigquery_client, dataset_id, table_id, processed_message)

            # Publish the processed message to the response topic
            publish_message(publisher, project_id, response_topic, processed_message)

            # Acknowledge the message after successful processing
            message.ack()
        except Exception as e:
            logging.error(f"Error in callback processing: {e}")
            # Optionally: Nack the message (send it back to the queue for reprocessing)
            message.nack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        streaming_pull_future.result()


# Main function to initialize and run the service
def main():
    setup_logging()

    # Load environment variables
    project_id, subscription_id, topic_name_request, topic_name_response, dataset_id, table_id = load_environment_variables()

    # Initialize clients
    publisher, subscriber = initialize_pubsub_clients()
    bigquery_client = initialize_bigquery_client()

    # Start subscribing to the request topic and handle messages
    subscribe_to_messages(subscriber, project_id, subscription_id, publisher, topic_name_response, bigquery_client,
                          dataset_id, table_id)


if __name__ == "__main__":
    main()
