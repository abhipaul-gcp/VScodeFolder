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

bucket_name = 'test-bucket-zee9'
project_id = 'cloudsec-2'
create_dlp_job(bucket_name, project_id)