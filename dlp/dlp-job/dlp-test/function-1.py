import base64
import functions_framework
import json
from google.cloud import storage

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    # Decode the data from Pub/Sub
    data = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
    # Parse the JSON data
    json_data = json.loads(data)
    # Extract the required fields
    bucket_name = json_data["resource"]["labels"]["bucket_name"]
    project_id = json_data["resource"]["labels"]["project_id"]
    # Get the bucket tag using the Google Cloud Storage client library
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    bucket_tag = bucket.labels
    # Print the bucket tag
    print(f"Bucket tag: {bucket_tag}")

    # Check for exceptation Tag
    ex_tag = bucket_tag.get("exception")

    if ex_tag and ex_tag == "dlp":
        print("Bucket exception tag found: ", ex_tag)
    else:
        print("No DLP exceptation tag found. Tag =", ex_tag)