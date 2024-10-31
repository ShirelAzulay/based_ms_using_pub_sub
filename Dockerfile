# Step 1: Use Python slim image as the base
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the rest of the code
COPY . .

# Step 5: Set environment variables (these can be replaced in Cloud Run or Kubernetes)
ENV GCP_PROJECT_ID=your-gcp-project-id
ENV PUBSUB_SUBSCRIPTION_ID=your-subscription-id
ENV PUBSUB_TOPIC_REQUEST=your-topic-request
ENV PUBSUB_TOPIC_RESPONSE=your-topic-response
ENV BIGQUERY_DATASET_ID=your-dataset-id
ENV BIGQUERY_TABLE_ID=your-table-id

# Step 6: Define the command to run the application
CMD ["python", "main.py"]
