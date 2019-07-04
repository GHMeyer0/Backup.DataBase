import logging
import boto3
import Utilities.System as sys
import Utilities.Mail as mail
from botocore.exceptions import ClientError

global client
client = boto3.client(
    's3',
    aws_access_key_id='',
    aws_secret_access_key=''
)
def upload_file(file_name, bucket, object_name, log):

    client = boto3.client('s3')
    sys.write_log_file("Start Upload to aws s3: Bucket" + bucket ,log)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        sys.write_log_file("Fail on Upload to aws s3: Bucket" + bucket ,log)
        
        exit()
    sys.write_log_file("Finish Upload to aws s3: Bucket" + bucket ,log)
    return True

upload_file("C:\Backup\.sql","mssql-backup-","teste/.sql")
