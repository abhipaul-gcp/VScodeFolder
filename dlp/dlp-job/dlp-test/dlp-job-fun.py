import base64
import functions_framework
import json
from google.cloud import storage
from google.cloud import dlp_v2

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

        create_dlp_job(bucket_name, project_id)

# Function to create dlp Job after getting input from pub-sub

from google.cloud import dlp_v2

def create_dlp_job(bucket_name, project_id):
    client = dlp_v2.DlpServiceClient()

    #project_id = 'cloudsec-2'

    # Working Copy without new file scan
    schedule = {'recurrence_period_duration': '2592000s'}
    actions = [{'publish_summary_to_cscc': {}}]
    info_types = []
    min_likelihood = 'POSSIBLE'
    custom_info_types = []
    inspect_template_name = 'projects/cloudsec-1/locations/global/inspectTemplates/zee-dlp'
    #bucket_name = 'test-bucket-zee3'
    include_regex = []
    exclude_regex = []
    file_types = [
        'BINARY_FILE',
        'TEXT_FILE',
        'IMAGE',
        'WORD',
        'PDF',
        'AVRO',
        'CSV',
        'TSV',
        'EXCEL',
        'POWERPOINT'
    ]
    files_limit_percent = 70
    sample_method = 'RANDOM_START'
    bytes_limit_per_file = '26843545600'

    file_set = {
        'regex_file_set': {
            'bucket_name': bucket_name,
            'include_regex': include_regex,
            'exclude_regex': exclude_regex
        }
    }

    storage_config = {
        'cloud_storage_options': {
            'files_limit_percent': files_limit_percent,
            'sample_method': sample_method,
            'bytes_limit_per_file': bytes_limit_per_file,
            'file_types': file_types,
            'file_set': file_set
        }
    }

    inspect_config = {
        'info_types': info_types,
        'min_likelihood': min_likelihood,
        'custom_info_types': custom_info_types
    }

    inspect_job = {
        'actions': actions,
        'inspect_config': inspect_config,
        'inspect_template_name': inspect_template_name,
        'storage_config': storage_config
    }

    job_trigger = {
        'triggers': [{'schedule': schedule}],
        'inspect_job': inspect_job
    }

    parent = f'projects/{project_id}'
    trigger = client.create_job_trigger(parent=parent, job_trigger=job_trigger)

    print(f'DLP job trigger created: {trigger.name}')

# bucket_name = 'test-bucket-zee9'
# project_id = 'cloudsec-2'
# create_dlp_job(bucket_name, project_id)