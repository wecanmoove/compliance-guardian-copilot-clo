"""Document text extraction utility."""
from pathlib import Path


ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.md'}


def is_allowed(filename: str) -> bool:
    """Check if file type is allowed."""
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS


def extract_text(filename: str, content: bytes) -> str:
    """Extract text from document."""
    ext = Path(filename).suffix.lower()

    if ext in {'.txt', '.md'}:
        return content.decode('utf-8', errors='ignore')

    elif ext == '.pdf':
        try:
            import PyPDF2
            from io import BytesIO
            reader = PyPDF2.PdfReader(BytesIO(content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Failed to extract PDF: {e}")

    elif ext == '.docx':
        try:
            from docx import Document
            from io import BytesIO
            doc = Document(BytesIO(content))
            text = "\n".join(para.text for para in doc.paragraphs)
            return text
        except Exception as e:
            raise ValueError(f"Failed to extract DOCX: {e}")

    else:
        raise ValueError(f"Unsupported file type: {ext}")
