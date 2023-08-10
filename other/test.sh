# GCP command to create CSR from KMS private key



# Create a KMS keyring and key
gcloud kms keyrings create [KEYRING_NAME] --location [LOCATION]
gcloud kms keys create [KEY_NAME] --location [LOCATION] --keyring [KEYRING_NAME] --purpose encryption

# Get the KMS key version and set it to a variable
KMS_KEY_VERSION=$(gcloud kms keys versions list --location northamerica-northeast1 --keyring test-assmetric-key --key my-key --format='value(name)')

# Generate the CSR using the KMS private key 
gcloud beta compute ssl-certificates create my-key.crt --domains "HDFC" --key-version $KMS_KEY_VERSION


gcloud kms certs create "self-signed-cert.crt" --key "my-key" --project "abhishekpaul"

# gcp command to generate a self signed by retrieving the existing key from KMS

# Generate a self-signed certificate by retrieving the existing key from KMS

gcloud kms keys versions list --keyring [KEYRING_NAME] --location [LOCATION] --key [KEY_NAME] \

gcloud kms keys versions list  --keyring "test-assmetric-key" --location "northamerica-northeast1" --key "my-key" | grep "^[0-9]" | tail -1 | awk '{print $2}'| xargs gcloud kms decrypt --ciphertext-file=- --plaintext-file=- | openssl req -new -x509 -nodes -days 365 -key /dev/stdin > selfsigned.crt