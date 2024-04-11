import os
import boto3
from botocore.exceptions import ClientError
import logging
import secret

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client(
    service_name='s3', region_name='ap-northeast-2',
    aws_access_key_id=secret.AWS_ACCESS_KEY_ID, aws_secret_access_key=secret.AWS_SECRET_ACCESS_KEY)
    
    try:
        with open("output/73c5573e-7/point_cloud/iteration_7000/" + file_name, "rb") as f:
            response = s3_client.upload_fileobj(f, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(file_name,bucket, object_name=None):
    
    if object_name is None:
        object_name = os.path.basename(file_name)
    
    s3_client = boto3.client(
    service_name='s3', region_name='ap-northeast-2',
    aws_access_key_id=secret.AWS_ACCESS_KEY_ID, aws_secret_access_key=secret.AWS_SECRET_ACCESS_KEY)
    
    try:
        with open("data/sample2/"+ file_name, "wb") as f:
            s3_client.download_fileobj(bucket, object_name, f)
    except ClientError as e:
        logging.error(e)
        return False
    return True