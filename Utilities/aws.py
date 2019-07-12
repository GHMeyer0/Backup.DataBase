import logging
import boto3
from boto3.s3.transfer import TransferConfig
import utilities.system as system
import utilities.mail as mail
from botocore.exceptions import ClientError
import os
import sys
import threading

import configuration.aws as aws_config

def upload_file_to_s3(file_path, file_name, s3_bucket, object_name):
    client = boto3.client(
        's3',
        aws_access_key_id=aws_config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_config.AWS_SECRET_ACCESS_KEY
    )

    config = TransferConfig(multipart_threshold=1024*25,
                            max_concurrency=10,
                            multipart_chunksize=1024*25, 
                            use_threads=True)
    system.write_log_file("Start Upload to aws s3: Bucket" + s3_bucket, file_path)
    try:
        response = client.upload_file(
            file_path + file_name,
            s3_bucket,
            object_name,
            Config = config,
            Callback=ProgressPercentage(file_path + file_name))
        print(response)
    except ClientError as e:
        logging.error(e)
        system.write_log_file(e + s3_bucket ,file_path)
        system.write_log_file(response + s3_bucket ,file_path)
        system.write_log_file("Fail on Upload to aws s3: Bucket" + s3_bucket, file_path)
        exit()
    system.write_log_file("Finish Upload to aws s3: Bucket" + s3_bucket ,file_path)
    return True

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()
