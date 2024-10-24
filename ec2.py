import os
import sys
import zipfile
import shutil
import boto3
from datetime import datetime

def get_latest_zip_file_from_s3(bucket_name, folder_name):
    """Get the latest ZIP file in the specified S3 folder."""
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name + '/')

    zip_files = []
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].endswith('.zip'):
                zip_files.append(obj['Key'])
    
    # Sort zip files by filename in descending order based on the timestamp 
    latest_zip_file = None
    if zip_files:
        latest_zip_file = max(zip_files, key=lambda x: datetime.strptime(x.split('/')[-1][:-4], '%Y%m%d_%H%M%S'), default=None)

    return latest_zip_file

def download_zip_file(s3_client, bucket_name, zip_file_key, local_file_path):
    """Download the latest ZIP file from S3 to the specified local path."""
    s3_client.download_file(bucket_name, zip_file_key, local_file_path)
    return local_file_path

def extract_zip_file(zip_file_path, extract_folder):
    """Extract the contents of the ZIP file to the specified folder."""
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

def main(project_name):
    bucket_name = 'sam-cd-bucket'
    folder_name = project_name
    latest_zip_file = get_latest_zip_file_from_s3(bucket_name, folder_name)
    
    if latest_zip_file:
        print(f"The latest ZIP file in 's3://{bucket_name}/{folder_name}':")
        print(f"  - {latest_zip_file}")
        
        local_folder_path = project_name
        if os.path.exists(local_folder_path):
            shutil.rmtree(local_folder_path)  
        os.makedirs(local_folder_path)

        # Download the latest ZIP file to the local folder
        s3_client = boto3.client('s3')
        local_zip_file_path = os.path.join(local_folder_path, os.path.basename(latest_zip_file))
        download_zip_file(s3_client, bucket_name, latest_zip_file, local_zip_file_path)
        print(f"Downloaded ZIP file to: {local_zip_file_path}")
        
        # Extract the contents of the ZIP file
        extract_zip_file(local_zip_file_path, local_folder_path)
        print(f"Extracted contents to: {local_folder_path}")
        
        # Remove the ZIP file after extraction
        os.remove(local_zip_file_path)
        print(f"Removed the ZIP file: {local_zip_file_path}")
    else:
        print(f"No ZIP files found in 's3://{bucket_name}/{folder_name}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Project name must be provided as an argument.")
        sys.exit(1)

    project_name_arg = sys.argv[1]
    main(project_name_arg)
