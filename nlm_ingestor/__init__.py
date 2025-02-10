from nlm_ingestor.ingestor import ingestor_api
import pypdfium2 as pdfium
from llmsherpa.readers import Document


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
    # estimate the total length
    txt_len = get_file_len(input_file)
    if txt_len == 0:
        raise ValueError("File does not contain text")

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