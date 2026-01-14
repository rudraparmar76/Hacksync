from preprocessing.summarizer import summarize_document
from preprocessing.loader import _extract_pdf

with open("test.pdf", "rb") as f:
    pdf_bytes = f.read()

text = _extract_pdf(pdf_bytes)
result = summarize_document(text)

print(result["summary"])
print(result["sections"])
