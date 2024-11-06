import os
import logging

# Load and validate environment variables
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
PUBSUB_SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID")
PUBSUB_TOPIC_REQUEST = os.getenv("PUBSUB_TOPIC_REQUEST")
PUBSUB_TOPIC_RESPONSE = os.getenv("PUBSUB_TOPIC_RESPONSE")
DATASET_NAME = os.getenv("DATASET_NAME")
TABLE_NAME = "satellite_data"

if not all([GCP_PROJECT_ID, PUBSUB_SUBSCRIPTION_ID, PUBSUB_TOPIC_REQUEST, PUBSUB_TOPIC_RESPONSE, DATASET_NAME]):
    logging.error("One or more environment variables are missing.")
    raise EnvironmentError("One or more environment variables are missing.")

# Optional configuration settings (logging, timeout values, etc.)
LOGGING_LEVEL = logging.INFO
