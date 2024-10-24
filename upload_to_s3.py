import os
import zipfile
import boto3
from datetime import datetime

def load_gitignore(gitignore_path):
    """Load .gitignore entries from a file."""
    ignore_patterns = []
    try:
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):  # Ignore comments and empty lines
                    ignore_patterns.append(line)
    except FileNotFoundError:
        print(f"No .gitignore file found at {gitignore_path}.")
    return ignore_patterns

def should_ignore(file_path, ignore_patterns):
    """Determine if a file should be ignored based on .gitignore patterns."""
    for pattern in ignore_patterns:
        if pattern in file_path:
            print(f"Ignoring '{file_path}' due to pattern '{pattern}'")  # Debugging line
            return True
    return False

def zip_project_files(source_dir, zip_file_path, ignore_patterns):
    """Create a zip file of all files in the specified directory, excluding ignored files."""
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                flag = True
                for pattern in ignore_patterns:
                    if pattern in file_path:
                        flag = False
                        break
                if flag:
                    arcname = os.path.relpath(file_path, start=source_dir)
                    zip_file.write(file_path, arcname)

def upload_to_s3(bucket_name, file_path, s3_object_name):
    """Upload a file to an S3 bucket."""
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, s3_object_name)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_object_name}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

def main():
    bucket_name = 'sam-cd-bucket'
    source_directory = './fastapi-server'
    project_name = 'fastapi-server'
    gitignore_path = os.path.join(source_directory, '.gitignore')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_file_name = f"{project_name}/{timestamp}.zip"
    zip_file_path = os.path.join(os.getcwd(), f"{timestamp}.zip")
    ignore_patterns = load_gitignore(gitignore_path)
    zip_project_files(source_directory, zip_file_path, ignore_patterns)

    upload_to_s3(bucket_name, zip_file_path, zip_file_name)
    os.remove(zip_file_path)

if __name__ == "__main__":
    main()
