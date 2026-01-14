import io
import pandas as pd
from pypdf import PdfReader
from docx import Document

def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Converts uploaded files into plain text.
    Supported formats: TXT, PDF, DOCX, CSV
    """

    filename = filename.lower()

    if filename.endswith(".pdf"):
        return _extract_pdf(file_bytes)

    if filename.endswith(".docx"):
        return _extract_docx(file_bytes)

    if filename.endswith(".csv"):
        return _extract_csv(file_bytes)

    # Default: treat as text
    return _extract_txt(file_bytes)


# ------------------ helpers ------------------

def _extract_txt(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def _extract_pdf(file_bytes: bytes) -> str:
    text = ""
    with io.BytesIO(file_bytes) as stream:
        reader = PdfReader(stream)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def _extract_docx(file_bytes: bytes) -> str:
    text = ""
    with io.BytesIO(file_bytes) as stream:
        doc = Document(stream)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text


def _extract_csv(file_bytes: bytes) -> str:
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
        return df.to_string(index=False)
    except Exception:
        return ""
