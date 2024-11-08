import logging
from clients import initialize_pubsub_clients, initialize_bigquery_client, initialize_gcs_client
from operations.pubsub_operations import subscribe_to_messages
from operations.gcs_operations import upload_file_to_gcs, download_file_from_gcs, list_files_in_gcs_bucket
import config

def setup_logging():
    """
    Sets up logging configuration based on the defined level in the config.
    """
    logging.basicConfig(level=config.LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging is set up.")

def load_environment_variables():
    """
    Validates that all required environment variables are loaded.
    """
    required_vars = [
        config.GCP_PROJECT_ID,
        config.PUBSUB_SUBSCRIPTION_ID,
        config.PUBSUB_TOPIC_REQUEST,
        config.PUBSUB_TOPIC_RESPONSE,
        config.DATASET_NAME,
        config.BUCKET_NAME
    ]

    if not all(required_vars):
        logging.error("One or more environment variables are missing.")
        raise EnvironmentError("One or more environment variables are missing.")
    logging.info("Environment variables loaded successfully.")

def example_gcs_operations(gcs_client):
    """
    Demonstrates example GCS operations such as upload, download, and listing files.
    """
    logging.info("Starting example GCS operations...")
    # Upload example
    source_file = "local-file.txt"  # Path to your local file
    destination_blob = "uploaded-file.txt"
    upload_file_to_gcs(gcs_client, config.BUCKET_NAME, source_file, destination_blob)

    # Download example
    source_blob = "uploaded-file.txt"
    destination_file = "downloaded-file.txt"
    download_file_from_gcs(gcs_client, config.BUCKET_NAME, source_blob, destination_file)

    # List files in the bucket
    files = list_files_in_gcs_bucket(gcs_client, config.BUCKET_NAME)
    logging.info(f"Files in GCS bucket {config.BUCKET_NAME}: {files}")

def main():

    setup_logging()

    load_environment_variables()

    # Initialize clients
    logging.info("Initializing clients...")
    publisher, subscriber = initialize_pubsub_clients()
    bigquery_client = initialize_bigquery_client()
    gcs_client = initialize_gcs_client()

    # Example usage of GCS operations
    example_gcs_operations(gcs_client)

    # Start subscribing to Pub/Sub messages
    logging.info("Starting to subscribe to Pub/Sub messages...")
    subscribe_to_messages(
        subscriber=subscriber,
        subscription_id=config.PUBSUB_SUBSCRIPTION_ID,
        publisher=publisher,
        response_topic=config.PUBSUB_TOPIC_RESPONSE,
        bigquery_client=bigquery_client,
        gcs_client=gcs_client
    )

if __name__ == "__main__":
    main()
