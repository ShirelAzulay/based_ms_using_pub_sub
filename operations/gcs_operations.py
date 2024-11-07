from google.cloud import storage
import logging


# Upload a file to GCS
def upload_file_to_gcs(gcs_client, bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a file to the specified GCS bucket.

    :param gcs_client: Initialized GCS client.
    :param bucket_name: Name of the bucket to upload to.
    :param source_file_name: Local path of the file to upload.
    :param destination_blob_name: The name to give the file in GCS.
    """
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_filename(source_file_name)
        logging.info(f"File {source_file_name} uploaded to {destination_blob_name}.")
    except Exception as e:
        logging.error(f"Failed to upload {source_file_name} to {destination_blob_name}: {e}")


# Download a file from GCS
def download_file_from_gcs(gcs_client, bucket_name, source_blob_name, destination_file_name):
    """
    Downloads a file from the specified GCS bucket.

    :param gcs_client: Initialized GCS client.
    :param bucket_name: Name of the bucket to download from.
    :param source_blob_name: The name of the file in GCS.
    :param destination_file_name: Local path to save the downloaded file.
    """
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    try:
        blob.download_to_filename(destination_file_name)
        logging.info(f"File {source_blob_name} downloaded to {destination_file_name}.")
    except Exception as e:
        logging.error(f"Failed to download {source_blob_name} to {destination_file_name}: {e}")


# List files in a GCS bucket
def list_files_in_gcs_bucket(gcs_client, bucket_name):
    """
    Lists all files in the specified GCS bucket.

    :param gcs_client: Initialized GCS client.
    :param bucket_name: Name of the bucket to list files from.
    :return: List of file names in the bucket.
    """
    bucket = gcs_client.bucket(bucket_name)

    try:
        blobs = bucket.list_blobs()
        file_names = [blob.name for blob in blobs]
        logging.info(f"Files in bucket {bucket_name}: {file_names}")
        return file_names
    except Exception as e:
        logging.error(f"Failed to list files in bucket {bucket_name}: {e}")
        return []

