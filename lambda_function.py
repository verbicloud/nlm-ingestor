from pathlib import Path
import uuid

import boto3
from nlm_ingestor.ingestor import ingestor_api
from llmsherpa.readers import Document


def parse_document(input_file):
    parse_options = {
        "parse_and_render_only": True,
        "render_format": "all",
        "use_new_indent_parser": False,
        "parse_pages": (),
        "apply_ocr": False,
    }

    return_dict, _ = ingestor_api.ingest_document(
        input_file,
        input_file,
        "application/pdf",
        parse_options=parse_options,
    )

    doc = Document(return_dict["result"]["blocks"])
    return doc.to_html()


def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    s3_bucket = event["bucket"]
    s3_filename = event["filename"]

    this_file = s3_client.get_object(Bucket=s3_bucket, Key=s3_filename)
    content = this_file["Body"].read()

    temp_filename = Path(f"/tmp/{uuid.uuid4()}.pdf")
    temp_filename.write_bytes(content)

    return parse_document(str(temp_filename))
