# My Python Pub/Sub and BigQuery Service

## Overview

This project is a Python-based microservice that:
- Listens to a Google Cloud Pub/Sub `request topic`.
- Processes messages received from the topic.
- Inserts the processed data into BigQuery.
- Publishes a response to a Pub/Sub `response topic`.

The project is containerized using Docker, allowing you to run it locally or deploy it to Google Cloud (such as Cloud Run).

## Prerequisites

Before running the project, make sure you have the following:

1. **Python 3.9+**
2. **Docker** installed on your machine.
3. A **Google Cloud Project** with:
   - Pub/Sub topics and subscriptions set up.
   - A BigQuery dataset and table.
4. **Google Cloud SDK** (if deploying to Google Cloud).
5. **Poetry** installed on your machine:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-repo/my-python-pubsub-project.git
   cd my-python-pubsub-project

2. **Create a virtual environment (optional but recommended)**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   
3. **Install dependencies**:

    ```bash
   pip install --upgrade pip
   ```
    ```bash
   poetry install
   ```
   
## Running - 

## 1. **Running the Project Locally**
#### You can run the project directly from Python if you have set up the necessary Google Cloud environment variables on your local machine.
```bash 
    poetry run python main.py
```
Ensure the following environment variables are set either in your system or in a .env file (with tools like dotenv):
GCP_PROJECT_ID: Your GCP project ID.
PUBSUB_SUBSCRIPTION_ID: Your Pub/Sub subscription ID for the request topic.
PUBSUB_TOPIC_REQUEST: Your Pub/Sub request topic name.
PUBSUB_TOPIC_RESPONSE: Your Pub/Sub response topic name.
BIGQUERY_DATASET_ID: Your BigQuery dataset ID.
BIGQUERY_TABLE_ID: Your BigQuery table ID.



    
## 2. **Run the Docker container locally**
### After building the Docker image, you can run the service locally using Docker:
    
```bash 
     docker run -it --rm \
        -e GCP_PROJECT_ID=your-gcp-project-id \
        -e PUBSUB_SUBSCRIPTION_ID=your-subscription-id \
        -e PUBSUB_TOPIC_REQUEST=your-topic-request \
        -e PUBSUB_TOPIC_RESPONSE=your-topic-response \
        -e BIGQUERY_DATASET_ID=your-dataset-id \
        -e BIGQUERY_TABLE_ID=your-table-id \
        my-python-service
  ```

#### Make sure to replace the environment variable values with the correct values for your Google Cloud project.

## 3.**Deploying to Google Cloud**
### You can deploy the Docker container to Google Cloud's Cloud Run for a serverless deployment, or Google Kubernetes Engine (GKE) for more control over scaling and networking.

## 4. **Deploying to Cloud Run**
  ### 4.1.  **Build and push the Docker image to Google Container Registry (GCR):**
First, tag the image and push it to GCR:
 ```bash
    docker tag my-python-service gcr.io/your-gcp-project-id/my-python-service
    docker push gcr.io/your-gcp-project-id/my-python-service
  ```


### 4.2.  **Once the image is pushed, deploy it to Cloud Run using the following command:**
```bash 
gcloud run deploy my-python-service \
    --image gcr.io/your-gcp-project-id/my-python-service \
    --platform managed \
    --region us-central1 \
    --set-env-vars GCP_PROJECT_ID=your-gcp-project-id,PUBSUB_SUBSCRIPTION_ID=your-subscription-id,PUBSUB_TOPIC_REQUEST=your-topic-request,PUBSUB_TOPIC_RESPONSE=your-topic-response,BIGQUERY_DATASET_ID=your-dataset-id,BIGQUERY_TABLE_ID=your-table-id
  ```

Replace your-gcp-project-id, your-subscription-id, and other environment variables with the actual values.
Cloud Run will automatically scale your service based on the incoming traffic.
Environment Variables
Make sure to set the following environment variables in your system or in the deployment platform:

#### GCP_PROJECT_ID: Your Google Cloud Project ID.
#### PUBSUB_SUBSCRIPTION_ID: Pub/Sub subscription ID for the request topic.
#### PUBSUB_TOPIC_REQUEST: Pub/Sub topic name for the request messages.
#### PUBSUB_TOPIC_RESPONSE: Pub/Sub topic name for the response messages.
#### BIGQUERY_DATASET_ID: BigQuery dataset ID for storing processed messages.
#### BIGQUERY_TABLE_ID: BigQuery table ID for storing processed messages.

```
Project Structure
/my-python-pubsub-project/
│
├── main.py                 # Main file to run the service
├── Dockerfile              # Dockerfile for building the container
├── requirements.txt        # Python dependencies
└── utils/                  # Optional helper scripts
    └── some_helper.py      # Example of a helper module
``` 


#### Logs and Monitoring
#### For Google Cloud deployments, it is recommended to integrate with Google Cloud Logging for tracking errors and service health. By default, Cloud Run and other GCP services integrate directly with Cloud Logging, and you can view logs via the Cloud Console.

#### For local deployments, logs are printed to the console, and you can adjust the logging levels inside main.py.