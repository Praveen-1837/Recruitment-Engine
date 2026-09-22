import os
import uuid
import logging
from typing import List
from uuid import UUID
import aiofiles
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import settings
from models.database import get_db, JobPosting, Candidate
from services.file_processor import validate_file, extract_text_from_file, FileProcessingError

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Candidates & Uploads"])

@router.post("/api/upload", status_code=status.HTTP_201_CREATED)
async def upload_resumes(
    files: List[UploadFile] = File(...),
    job_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload 1-50 resumes (PDF, DOCX, TXT) for a job posting.
    Validates, extracts text, creates Candidate records, and deletes temporary files.
    Conforms to TechSpec.md Section 3.2 and Rules.md Section 2.1.
    """
    try:
        parsed_job_id = UUID(job_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "code": "INVALID_JOB_ID", "message": "job_id must be a valid UUID."}
        )

    # Check that job exists
    job = db.query(JobPosting).filter(JobPosting.id == parsed_job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "code": "JOB_NOT_FOUND", "message": f"Job with ID '{job_id}' not found."}
        )

    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "code": "NO_FILES_PROVIDED", "message": "At least one file must be uploaded."}
        )

    if len(files) > settings.max_resumes_per_batch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": True,
                "code": "BATCH_LIMIT_EXCEEDED",
                "message": f"Maximum allowed batch size is {settings.max_resumes_per_batch} resumes."
            }
        )

    uploaded_files_info = []
    errors = []

    for file in files:
        temp_file_path = None
        try:
            filename = file.filename or "unknown_resume.txt"
            # Read file content to check size and write temporary file
            content = await file.read()
            file_size = len(content)

            # Validate file extension and size
            validate_file(filename, file.content_type or "", file_size)

            # Save to temporary path for processing
            temp_filename = f"{uuid.uuid4()}_{filename}"
            temp_file_path = os.path.join(settings.upload_dir, temp_filename)
            
            async with aiofiles.open(temp_file_path, "wb") as f:
                await f.write(content)

            # Extract clean text
            extracted_text = extract_text_from_file(temp_file_path, filename)

            # Create Candidate record
            candidate = Candidate(
                job_id=parsed_job_id,
                filename=filename,
                original_text=extracted_text,
                extracted_skills={},  # Will be populated during analyze phase
                experience_years=0,
                certification_count=0
            )
            db.add(candidate)
            db.commit()
            db.refresh(candidate)

            uploaded_files_info.append({
                "filename": filename,
                "candidate_id": str(candidate.id),
                "size_bytes": file_size
            })

        except FileProcessingError as fpe:
            logger.warning(f"File validation/processing error on {file.filename}: {fpe.message}")
            errors.append(f"{file.filename}: {fpe.message}")
        except Exception as e:
            logger.error(f"Unexpected error processing {file.filename}: {str(e)}")
            errors.append(f"{file.filename}: {str(e)}")
        finally:
            # Delete temporary file immediately after text extraction (Rules.md Section 2.1)
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception as del_err:
                    logger.warning(f"Failed to remove temp file {temp_file_path}: {del_err}")

    if not uploaded_files_info and errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "code": "UPLOAD_FAILED", "message": "; ".join(errors)}
        )

    return {
        "success": True,
        "data": {
            "job_id": str(parsed_job_id),
            "uploaded_files": uploaded_files_info,
            "total_uploaded": len(uploaded_files_info),
            "failed": len(errors),
            "errors": errors
        },
        "message": f"Successfully uploaded {len(uploaded_files_info)} resumes."
    }

@router.get("/api/candidates/{job_id}")
def get_job_candidates(job_id: UUID, db: Session = Depends(get_db)):
    """Retrieve list of candidates uploaded for a specific job."""
    candidates = db.query(Candidate).filter(Candidate.job_id == job_id).order_by(Candidate.created_at.desc()).all()
    
    results = []
    for c in candidates:
        results.append({
            "id": str(c.id),
            "candidate_id": str(c.id),
            "job_id": str(c.job_id),
            "filename": c.filename,
            "experience_years": c.experience_years,
            "certification_count": c.certification_count,
            "has_extracted_skills": bool(c.extracted_skills and len(c.extracted_skills) > 0),
            "created_at": c.created_at.isoformat()
        })
        
    return {
        "success": True,
        "data": results,
        "total": len(results)
    }

@router.get("/api/candidates/detail/{candidate_id}")
def get_candidate_detail(candidate_id: UUID, db: Session = Depends(get_db)):
    """Retrieve complete candidate information including skills and text preview."""
    cand = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not cand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "code": "CANDIDATE_NOT_FOUND", "message": "Candidate not found."}
        )

    return {
        "success": True,
        "data": {
            "candidate_id": str(cand.id),
            "id": str(cand.id),
            "job_id": str(cand.job_id),
            "filename": cand.filename,
            "extracted_skills": cand.extracted_skills,
            "experience_years": cand.experience_years,
            "certification_count": cand.certification_count,
            "text_preview": cand.original_text[:1000] if cand.original_text else "",
            "created_at": cand.created_at.isoformat()
        }
    }
