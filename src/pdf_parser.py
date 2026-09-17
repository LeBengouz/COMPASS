import pymupdf4llm


def pdf_to_markdown(pdf_path):
    # pdf_path : string of the path to the pdf
    md = pymupdf4llm.to_markdown(pdf_path)
    return md