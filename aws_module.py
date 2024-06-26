import os
import boto3
from botocore.exceptions import ClientError
import logging
import secret
import time



def upload_file(file_name, bucket, object_name=None):
    
    if(secret.ITERATION == 30_000):
        iteration = "30000"
    elif(secret.ITERATION == 7_000):
        iteration = "7000"
    
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client(
    service_name='s3', region_name='ap-northeast-2',
    aws_access_key_id=secret.AWS_ACCESS_KEY_ID, aws_secret_access_key=secret.AWS_SECRET_ACCESS_KEY)
    
    try:
        with open("output/"+object_name+"/point_cloud/iteration_"+iteration+"/point_cloud.ply" , "rb") as f:
            response = s3_client.upload_fileobj(f, bucket, object_name+".ply")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(file_name,bucket, object_name=None):
    
    if object_name is None:
        object_name = os.path.basename(file_name)
    
    os.mkdir("data/"+object_name)
    
    s3_client = boto3.client(
    service_name='s3', region_name='ap-northeast-2',
    aws_access_key_id=secret.AWS_ACCESS_KEY_ID, aws_secret_access_key=secret.AWS_SECRET_ACCESS_KEY)
    
    try:
        with open("data/"+ object_name + "/"+object_name+ ".mp4" , "wb") as f:
            s3_client.download_fileobj(bucket, object_name+".mp4", f)
            
    except ClientError as e:
        logging.error(e)
        return False
    os.mkdir("data/"+object_name+"/input")
    os.system("ffmpeg -i data/"+object_name+"/"+object_name+".mp4 -qscale:v 1 -qmin 1 -vf fps=2 "
              +"data/"+object_name+"/input/%04d.jpg")
    
    return object_name

if __name__ == "__main__":
    download_file("dkqcnrss", "3d-modeling-mall", "dkqcnrss")