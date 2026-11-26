import pymupdf


def extract_text_from_pdf(pdf_bytes):

    extracted_text = []

    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        for page in document:
            page_text = page.get_text("text")
            extracted_text.append(page_text)

    return "\n".join(extracted_text).strip()