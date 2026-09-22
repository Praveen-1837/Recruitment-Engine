from datetime import datetime, timezone
import logging
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.database import get_db, JobPosting, Candidate, JobMatch
from models.schemas import CompareRequest
from services.skill_extractor import extract_skills_from_resume, extract_requirements_from_job
from services.matcher import calculate_match_score
from services.ranker import rank_candidates, generate_comparison_recommendation

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Analysis & Matching"])

@router.post("/api/analyze/{job_id}")
def analyze_candidates(job_id: UUID, db: Session = Depends(get_db)):
    """
    Orchestrate complete analysis pipeline:
    1. Extract skills from candidates if not already done.
    2. Extract requirements from job if missing.
    3. Calculate match score, matched/missing skills for each candidate.
    4. Rank candidates and generate assessment.
    5. Save results to job_matches table.
    Conforms to AppFlow.md Section 2.3 and TechSpec.md Section 3.4.
    """
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "code": "JOB_NOT_FOUND", "message": f"Job with ID '{job_id}' not found."}
        )

    candidates = db.query(Candidate).filter(Candidate.job_id == job_id).all()
    if not candidates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "code": "NO_CANDIDATES", "message": "No candidates uploaded for this job yet."}
        )

    # Ensure job requirements are present
    if not job.extracted_requirements or not job.extracted_requirements.get("required_technical_skills"):
        reqs = extract_requirements_from_job(job.description)
        job.extracted_requirements = reqs
        job.required_years_experience = reqs.get("minimum_years_experience", 0)
        job.seniority_level = reqs.get("preferred_seniority_level", "mid-level")
        db.commit()

    # Step 1: Ensure each candidate has extracted skills
    candidates_match_prep = []
    for cand in candidates:
        if not cand.extracted_skills or len(cand.extracted_skills.get("technical_skills", [])) == 0:
            skills = extract_skills_from_resume(cand.original_text)
            cand.extracted_skills = skills
            cand.experience_years = skills.get("years_experience", 0)
            cand.certification_count = len(skills.get("certifications", []))
            cand.updated_at = datetime.now(timezone.utc)
            db.commit()

        # Calculate match breakdown
        match_details = calculate_match_score(cand.extracted_skills, job.extracted_requirements)
        candidates_match_prep.append({
            "candidate": {
                "id": cand.id,
                "filename": cand.filename,
                "experience_years": cand.experience_years
            },
            "match_details": match_details
        })

    # Step 2: Rank candidates
    ranked_results = rank_candidates(candidates_match_prep)

    # Step 3: Persist to job_matches (clean up existing matches first)
    db.query(JobMatch).filter(JobMatch.job_id == job_id).delete()
    db.commit()

    for item in ranked_results:
        match_record = JobMatch(
            candidate_id=item["candidate_id"],
            job_id=job_id,
            match_score=item["match_score"],
            matched_skills=item["matched_skills"],
            missing_skills=item["missing_skills"],
            extra_skills=item["extra_skills"],
            assessment=item["assessment"],
            rank=item["rank"],
            created_at=datetime.now(timezone.utc)
        )
        db.add(match_record)
    db.commit()

    top_match = None
    if ranked_results:
        top_match = {
            "candidate_id": str(ranked_results[0]["candidate_id"]),
            "filename": ranked_results[0]["filename"],
            "match_score": ranked_results[0]["match_score"],
            "rank": 1
        }

    # Format JSON serializable candidate list
    formatted_candidates = []
    for r in ranked_results:
        formatted_candidates.append({
            "candidate_id": str(r["candidate_id"]),
            "filename": r["filename"],
            "rank": r["rank"],
            "match_score": r["match_score"],
            "matched_skills": r["matched_skills"],
            "missing_skills": r["missing_skills"],
            "extra_skills": r["extra_skills"],
            "matched_nice_to_have": r["matched_nice_to_have"],
            "experience_years": r["experience_years"],
            "experience_fit": r["experience_fit"],
            "assessment": r["assessment"]
        })

    return {
        "success": True,
        "data": {
            "job_id": str(job_id),
            "candidates_ranked": formatted_candidates,
            "analysis_completed_at": datetime.now(timezone.utc).isoformat(),
            "top_match": top_match
        },
        "message": f"Successfully analyzed and ranked {len(formatted_candidates)} candidates."
    }

@router.post("/api/compare")
def compare_candidates(request: CompareRequest, db: Session = Depends(get_db)):
    """
    Compare 2-3 candidates side-by-side.
    Conforms to TechSpec.md Section 3.6 and Design.md Section 2.6.
    """
    job = db.query(JobPosting).filter(JobPosting.id == request.job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "code": "JOB_NOT_FOUND", "message": "Job not found."}
        )

    if len(request.candidate_ids) < 1 or len(request.candidate_ids) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "code": "INVALID_CANDIDATE_COUNT", "message": "Please select 1 to 5 candidates to compare."}
        )

    comparison_data = []
    req_skills = job.extracted_requirements.get("required_technical_skills", [])

    for cid in request.candidate_ids:
        cand = db.query(Candidate).filter(Candidate.id == cid).first()
        if not cand:
            continue
        match = db.query(JobMatch).filter(JobMatch.candidate_id == cid, JobMatch.job_id == request.job_id).first()
        
        if match:
            score = match.match_score
            matched = match.matched_skills
            missing = match.missing_skills
            extra = match.extra_skills
            rank = match.rank
        else:
            calc = calculate_match_score(cand.extracted_skills, job.extracted_requirements)
            score = calc["match_score"]
            matched = calc["matched_skills"]
            missing = calc["missing_skills"]
            extra = calc["extra_skills"]
            rank = None

        comparison_data.append({
            "candidate_id": str(cand.id),
            "filename": cand.filename,
            "rank": rank,
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "extra_skills": extra,
            "years_experience": cand.experience_years or 0
        })

    recommendation = generate_comparison_recommendation(comparison_data, job.title)

    return {
        "success": True,
        "data": {
            "job_id": str(job.id),
            "job_title": job.title,
            "candidates": comparison_data,
            "required_skills": req_skills,
            "recommendation": recommendation
        }
    }
