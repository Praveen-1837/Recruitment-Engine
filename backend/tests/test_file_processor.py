import os
import pytest
from services.file_processor import (
    validate_file,
    clean_text,
    extract_text_from_file,
    FileProcessingError
)

def test_validate_file_valid():
    validate_file("resume.pdf", "application/pdf", 1024)
    validate_file("resume.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 2048)
    validate_file("resume.txt", "text/plain", 512)

def test_validate_file_invalid_extension():
    with pytest.raises(FileProcessingError) as exc:
        validate_file("resume.exe", "application/octet-stream", 1024)
    assert exc.value.code == "INVALID_FILE_TYPE"

def test_validate_file_empty():
    with pytest.raises(FileProcessingError) as exc:
        validate_file("resume.pdf", "application/pdf", 0)
    assert exc.value.code == "EMPTY_FILE"

def test_validate_file_too_large():
    with pytest.raises(FileProcessingError) as exc:
        validate_file("resume.pdf", "application/pdf", 15 * 1024 * 1024)
    assert exc.value.code == "FILE_TOO_LARGE"

def test_clean_text():
    raw = "  Hello \t\t world!\r\n\r\n\r\n\r\nThis   is   clean text.   "
    cleaned = clean_text(raw)
    assert cleaned == "Hello world!\n\nThis is clean text."

def test_extract_text_from_samples():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../test_data/resumes"))
    
    # PDF
    pdf_path = os.path.join(base_dir, "alex_senior_python.pdf")
    if os.path.exists(pdf_path):
        text = extract_text_from_file(pdf_path, "alex_senior_python.pdf")
        assert "Alex Chen" in text
        assert "FastAPI" in text

    # DOCX
    docx_path = os.path.join(base_dir, "sarah_mid_python.docx")
    if os.path.exists(docx_path):
        text = extract_text_from_file(docx_path, "sarah_mid_python.docx")
        assert "Sarah Jenkins" in text
        assert "Django" in text

    # TXT
    txt_path = os.path.join(base_dir, "jordan_junior_python.txt")
    if os.path.exists(txt_path):
        text = extract_text_from_file(txt_path, "jordan_junior_python.txt")
        assert "Jordan Miller" in text
        assert "Flask" in text
