from pathlib import Path

from nlm_ingestor.ingestor import ingestor_api


def parse_document(
    file=None,
    render_format: str = "all",
):
    render_format = "all"
    use_new_indent_parser = "no"
    apply_ocr = "no"

    parse_options = {
        "parse_and_render_only": True,
        "render_format": render_format,
        "use_new_indent_parser": use_new_indent_parser == "yes",
        "parse_pages": (),
        "apply_ocr": apply_ocr == "yes",
    }

    Path("/tmp/tmp.pdf").write_bytes(
        Path(file).read_bytes()
    )

    return_dict, _ = ingestor_api.ingest_document(
        "/tmp/tmp.pdf",
        "/tmp/tmp.pdf",
        "application/pdf",
        parse_options=parse_options,
    )

    return return_dict


if __name__ == "__main__":
    from argparse import ArgumentParser
    from llmsherpa.readers import Document

    parser = ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    file = parse_document(args.file)

    doc = Document(file["result"]["blocks"])
    print(doc.to_html(), flush=True)
