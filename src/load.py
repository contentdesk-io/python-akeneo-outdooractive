from os import getenv
from dotenv import find_dotenv, load_dotenv
import boto3
import xml.etree.ElementTree as ET
from transform import transformSingle
load_dotenv(find_dotenv())

S3_ENDPOINT = getenv('S3_ENDPOINT')
S3_BUCKET = getenv('S3_BUCKET')
S3_REGION = getenv('S3_REGION')
S3_ACCESS_KEY = getenv('S3_ACCESS_KEY')
S3_SECRET_ACCESS_KEY = getenv('S3_SECRET_ACCESS_KEY')
S3_EXPORT_PATH = getenv('S3_EXPORT_PATH')

def s3client():
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_ACCESS_KEY,
        endpoint_url='https://sos-'+S3_REGION+'.'+S3_ENDPOINT,
    )
    return s3_client

import xml.etree.ElementTree as ET

def puObject(data, bucket, filename):
    s3 = s3client()
    s3.put_object(
        Bucket=bucket,
        Key=filename,
        Body=data,
        ACL='public-read',
        ContentType='application/xml')

def load(products):
    print("Loading data to target")
    print(products)
    for product in products:
        print(product)
        transformData = transformSingle(product)
        puObject(transformData, S3_BUCKET, S3_EXPORT_PATH+product['identifier']+".xml")
        #createAndUploadXML(transformData, S3_EXPORT_PATH+product['identifier']+".xml")