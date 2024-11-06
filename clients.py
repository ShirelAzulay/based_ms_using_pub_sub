from google.cloud import pubsub_v1, bigquery
import logging

def initialize_pubsub_clients():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    logging.info("Pub/Sub clients initialized successfully.")
    return publisher, subscriber

def initialize_bigquery_client():
    bigquery_client = bigquery.Client()
    logging.info("BigQuery client initialized successfully.")
    return bigquery_client
