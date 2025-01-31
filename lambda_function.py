import tika

print("Starting tika serer")
tika.initVM()
from tempfile import NamedTemporaryFile
import boto3
from nlm_ingestor.ingestor import ingestor_api
import pypdfium2 as pdfium
from llmsherpa.readers import Document
import requests
import time

MAX_TEXT_LEN = 500000


def get_file_len(file):
    pdf = pdfium.PdfDocument(file)
    txt_len = 0

    for i in range(len(pdf)):
        page = pdf.get_page(i)
        txt_page = page.get_textpage()
        txt_len += len(txt_page.get_text_range().strip())

        if txt_len > MAX_TEXT_LEN:
            raise ValueError("Input file contains too much text")

    return txt_len


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

    tmpfile = NamedTemporaryFile(dir="/tmp", suffix=".pdf")
    tmpfile.write(content)

    # check if there is text in the PDF
    txt_len = get_file_len(tmpfile.name)
    if txt_len == 0:
        raise ValueError("File does not contain text")

    return parse_document(tmpfile.name)
