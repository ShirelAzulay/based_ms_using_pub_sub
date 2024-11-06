import logging
from clients import initialize_pubsub_clients, initialize_bigquery_client
from pubsub_operations import subscribe_to_messages
import config

def setup_logging():
    logging.basicConfig(level=config.LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging is set up.")

def main():
    setup_logging()

    # Initialize clients
    publisher, subscriber = initialize_pubsub_clients()
    bigquery_client = initialize_bigquery_client()

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
