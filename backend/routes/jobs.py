import uuid
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.database import get_db, JobPosting, Candidate, JobMatch
from models.schemas import JobCreateRequest, BaseSuccessResponse, JobResponseData
from services.skill_extractor import extract_requirements_from_job

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_job(request: JobCreateRequest, db: Session = Depends(get_db)):
    """
    Create a new job posting and extract requirements using Claude AI.
    Conforms to TechSpec.md Section 3.3.
    """
    try:
        # Extract requirements using Claude or fallback
        extracted = extract_requirements_from_job(request.description)
        min_years = extracted.get("minimum_years_experience", 0)
        seniority = extracted.get("preferred_seniority_level", "mid-level")

        job = JobPosting(
            title=request.title.strip(),
            description=request.description.strip(),
            extracted_requirements=extracted,
            required_years_experience=min_years,
            seniority_level=seniority
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        response_data = {
            "job_id": str(job.id),
            "id": str(job.id),
            "title": job.title,
            "description": job.description,
            "requirements_extracted": True,
            "required_skills": extracted.get("required_technical_skills", []),
            "required_soft_skills": extracted.get("required_soft_skills", []),
            "nice_to_have_skills": extracted.get("nice_to_have_skills", []),
            "minimum_years_experience": min_years,
            "seniority_level": seniority,
            "created_at": job.created_at.isoformat()
        }

        return {
            "success": True,
            "data": response_data,
            "message": "Job created and requirements extracted successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "code": "JOB_CREATION_FAILED", "message": str(e)}
        )

@router.get("")
def list_jobs(db: Session = Depends(get_db)):
    """List all created job postings with candidate counts."""
    jobs = db.query(JobPosting).order_by(JobPosting.created_at.desc()).all()
    results = []
    for j in jobs:
        c_count = db.query(func.count(Candidate.id)).filter(Candidate.job_id == j.id).scalar() or 0
        m_count = db.query(func.count(JobMatch.id)).filter(JobMatch.job_id == j.id).scalar() or 0
        results.append({
            "id": str(j.id),
            "job_id": str(j.id),
            "title": j.title,
            "description": j.description,
            "extracted_requirements": j.extracted_requirements,
            "required_years_experience": j.required_years_experience,
            "seniority_level": j.seniority_level,
            "created_at": j.created_at.isoformat(),
            "candidate_count": c_count,
            "is_analyzed": m_count > 0
        })

    return {
        "success": True,
        "data": results
    }

@router.get("/{job_id}")
def get_job(job_id: UUID, db: Session = Depends(get_db)):
    """Fetch details of a specific job posting."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "code": "JOB_NOT_FOUND", "message": f"Job with ID '{job_id}' not found."}
        )
    c_count = db.query(func.count(Candidate.id)).filter(Candidate.job_id == job.id).scalar() or 0
    m_count = db.query(func.count(JobMatch.id)).filter(JobMatch.job_id == job.id).scalar() or 0

    return {
        "success": True,
        "data": {
            "id": str(job.id),
            "job_id": str(job.id),
            "title": job.title,
            "description": job.description,
            "extracted_requirements": job.extracted_requirements,
            "required_years_experience": job.required_years_experience,
            "seniority_level": job.seniority_level,
            "created_at": job.created_at.isoformat(),
            "candidate_count": c_count,
            "is_analyzed": m_count > 0
        }
    }
