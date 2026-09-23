"""Text extraction from uploaded resume files (PDF, DOCX, TXT)."""
import pdfplumber


def extract_text_from_pdf(file_obj) -> str:
    """Extract raw text from a PDF file-like object."""
    text_chunks = []
    file_obj.seek(0)
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_chunks.append(page_text)
    return "\n".join(text_chunks).strip()


def extract_text_from_docx(file_obj) -> str:
    from docx import Document

    file_obj.seek(0)
    doc = Document(file_obj)
    return "\n".join(p.text for p in doc.paragraphs).strip()


def extract_text(file_obj, filename: str) -> str:
    """Dispatch extraction based on file extension."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_obj)
    if lower.endswith(".docx"):
        return extract_text_from_docx(file_obj)
    # Fallback: assume plain text
    file_obj.seek(0)
    raw = file_obj.read()
    if isinstance(raw, bytes):
        return raw.decode("utf-8", errors="ignore")
    return raw
