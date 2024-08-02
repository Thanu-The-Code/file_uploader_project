# file_uploader/uploader.py
import os
import boto3
from google.cloud import storage
from botocore.exceptions import NoCredentialsError

class FileUploader:
    def __init__(self, aws_access_key, aws_secret_key, s3_bucket_name, gcs_bucket_name, aws_region='us-east-1'):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        self.gcs_client = storage.Client()
        self.s3_bucket_name = s3_bucket_name
        self.gcs_bucket_name = gcs_bucket_name

    def upload_files(self, directory, s3_file_types, gcs_file_types):
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.split('.')[-1].lower() in s3_file_types:
                    self.upload_to_s3(file_path)
                elif file.split('.')[-1].lower() in gcs_file_types:
                    self.upload_to_gcs(file_path)

    def upload_to_s3(self, file_path):
        try:
            self.s3_client.upload_file(file_path, self.s3_bucket_name, os.path.basename(file_path))
            print(f"Uploaded {file_path} to S3 bucket {self.s3_bucket_name}")
        except FileNotFoundError:
            print(f"File {file_path} not found")
        except NoCredentialsError:
            print("Credentials not available")

    def upload_to_gcs(self, file_path):
        try:
            bucket = self.gcs_client.get_bucket(self.gcs_bucket_name)
            blob = bucket.blob(os.path.basename(file_path))
            blob.upload_from_filename(file_path)
            print(f"Uploaded {file_path} to GCS bucket {self.gcs_bucket_name}")
        except FileNotFoundError:
            print(f"File {file_path} not found")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")
