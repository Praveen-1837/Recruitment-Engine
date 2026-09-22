import os
import re
import logging
from typing import Tuple
import PyPDF2
from docx import Document
from config import settings

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
    "text/plain",
    "application/octet-stream"  # often sent by browsers for text/unknown files
}

class FileProcessingError(Exception):
    def __init__(self, message: str, code: str = "FILE_PROCESSING_ERROR"):
        super().__init__(message)
        self.message = message
        self.code = code

def validate_file(filename: str, content_type: str, file_size: int) -> None:
    """Validate file extension, mime type, and file size."""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise FileProcessingError(
            f"Unsupported file type '{ext}'. Allowed types: PDF, DOCX, TXT.",
            code="INVALID_FILE_TYPE"
        )
    
    if file_size <= 0:
        raise FileProcessingError("Uploaded file is empty.", code="EMPTY_FILE")

    if file_size > settings.max_file_size:
        raise FileProcessingError(
            f"File size exceeds limit of {settings.max_file_size // (1024 * 1024)}MB.",
            code="FILE_TOO_LARGE"
        )

def clean_text(raw_text: str) -> str:
    """Normalize extracted text by removing superfluous whitespace and non-standard characters."""
    if not raw_text:
        return ""
    # Replace carriage returns
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    # Replace tabs with spaces
    text = text.replace("\t", " ")
    # Replace multiple spaces with single space
    text = re.sub(r" +", " ", text)
    # Replace more than 2 consecutive newlines with 2 newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip leading/trailing whitespace
    return text.strip()

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file using PyPDF2."""
    text_fragments = []
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)
            if num_pages == 0:
                raise FileProcessingError("PDF contains no pages.", code="PDF_NO_PAGES")
            
            for idx, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        text_fragments.append(page_text.strip())
                except Exception as page_err:
                    logger.warning(f"Error extracting page {idx} from {file_path}: {page_err}")
                    continue
        
        extracted = "\n\n".join(text_fragments)
        return clean_text(extracted)
    except FileProcessingError:
        raise
    except Exception as e:
        logger.error(f"Failed to parse PDF {file_path}: {str(e)}")
        raise FileProcessingError(f"Error reading PDF file: {str(e)}", code="PDF_READ_ERROR")

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file using python-docx."""
    try:
        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        
        # Also extract table text if present
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join([cell.text.strip() for cell in row.cells if cell.text.strip()])
                if row_text:
                    paragraphs.append(row_text)
                    
        extracted = "\n\n".join(paragraphs)
        return clean_text(extracted)
    except Exception as e:
        logger.error(f"Failed to parse DOCX {file_path}: {str(e)}")
        raise FileProcessingError(f"Error reading DOCX file: {str(e)}", code="DOCX_READ_ERROR")

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from a plain TXT file."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()
        return clean_text(raw)
    except Exception as e:
        logger.error(f"Failed to parse TXT {file_path}: {str(e)}")
        raise FileProcessingError(f"Error reading TXT file: {str(e)}", code="TXT_READ_ERROR")

def extract_text_from_file(file_path: str, filename: str) -> str:
    """Extract, clean, and validate text from supported file types."""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    elif ext == ".txt":
        text = extract_text_from_txt(file_path)
    else:
        raise FileProcessingError(f"Unsupported file extension: {ext}", code="INVALID_FILE_TYPE")
        
    if not text or len(text) < 20:
        raise FileProcessingError(
            "Extracted text is empty or too short (<20 characters).",
            code="TEXT_EXTRACTION_FAILED"
        )
    
    # Cap text length to avoid token overflows
    if len(text) > 100000:
        text = text[:100000]
        
    return text
