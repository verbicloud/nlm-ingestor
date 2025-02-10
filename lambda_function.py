import tika

print("Starting tika serer")
tika.initVM()
from tempfile import NamedTemporaryFile
import boto3

import requests
from nlm_ingestor import parse_document


def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    s3_bucket = event["bucket"]
    s3_filename = event["filename"]

    this_file = s3_client.get_object(Bucket=s3_bucket, Key=s3_filename)
    content = this_file["Body"].read()

    with NamedTemporaryFile(dir="/tmp", suffix=".pdf") as tmpfile:
        tmpfile.write(content)

        # check if there is text in the PDF
        return parse_document(tmpfile.name)
