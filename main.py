import logging
from clients import initialize_pubsub_clients, initialize_bigquery_client, initialize_gcs_client
from pubsub_operations import subscribe_to_messages
from gcs_operations import upload_file_to_gcs, download_file_from_gcs, list_files_in_gcs_bucket
import config

def setup_logging():
    logging.basicConfig(level=config.LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging is set up.")

def upload_example_file(gcs_client):
    """Uploads an example file to GCS."""
    source_file = "local-file.txt"  # Path to your local file
    destination_blob = "uploaded-file.txt"
    upload_file_to_gcs(gcs_client, config.BUCKET_NAME, source_file, destination_blob)

def download_example_file(gcs_client):
    """Downloads an example file from GCS."""
    source_blob = "uploaded-file.txt"
    destination_file = "downloaded-file.txt"
    download_file_from_gcs(gcs_client, config.BUCKET_NAME, source_blob, destination_file)

def list_files_in_bucket(gcs_client):
    """Lists all files in the GCS bucket."""
    return list_files_in_gcs_bucket(gcs_client, config.BUCKET_NAME)

def main():
    setup_logging()

    # Initialize clients
    publisher, subscriber = initialize_pubsub_clients()
    bigquery_client = initialize_bigquery_client()
    gcs_client = initialize_gcs_client()

    # Example usage of GCS operations
    upload_example_file(gcs_client)
    download_example_file(gcs_client)
    list_files_in_bucket(gcs_client)

    # Start subscribing to Pub/Sub messages
    subscribe_to_messages(
        subscriber=subscriber,
        subscription_id=config.PUBSUB_SUBSCRIPTION_ID,
        publisher=publisher,
        response_topic=config.PUBSUB_TOPIC_RESPONSE,
        bigquery_client=bigquery_client,
    )

if __name__ == "__main__":
    main()
