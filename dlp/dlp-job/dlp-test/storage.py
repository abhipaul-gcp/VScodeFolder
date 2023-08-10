from google.cloud import storage

bucket_name = "test-bucket-zee9"
client = storage.Client()
bucket = client.get_bucket(bucket_name)
bucket_tag = bucket.labels

pii_tag = bucket_tag.get("pii")

if pii_tag and pii_tag == "aadhar":
    print("Bucket tag pii:", pii_tag)
else:
    print("No pii tag found . Tag =", pii_tag)
