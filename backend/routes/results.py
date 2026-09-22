import csv
import io
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from models.database import get_db, JobPosting, Candidate, JobMatch

router = APIRouter(tags=["Results & Exports"])

@router.get("/api/results/{job_id}")
def get_job_results(job_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve ranked candidate results for a given job posting.
    Conforms to TechSpec.md Section 3.4 and Design.md Section 2.4.
    """
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "code": "JOB_NOT_FOUND", "message": "Job not found."}
        )

    matches = db.query(JobMatch, Candidate).join(
        Candidate, JobMatch.candidate_id == Candidate.id
    ).filter(
        JobMatch.job_id == job_id
    ).order_by(
        JobMatch.rank.asc()
    ).all()

    results = []
    for match, candidate in matches:
        results.append({
            "candidate_id": str(candidate.id),
            "filename": candidate.filename,
            "rank": match.rank,
            "match_score": match.match_score,
            "matched_skills": match.matched_skills,
            "missing_skills": match.missing_skills,
            "extra_skills": match.extra_skills,
            "assessment": match.assessment,
            "experience_years": candidate.experience_years,
            "created_at": match.created_at.isoformat()
        })

    best_match = results[0] if results else None

    return {
        "success": True,
        "data": {
            "job_id": str(job.id),
            "job_title": job.title,
            "job_description": job.description,
            "extracted_requirements": job.extracted_requirements,
            "total_candidates": len(results),
            "best_match": best_match,
            "candidates": results
        }
    }

@router.get("/api/export/{job_id}")
def export_job_results(
    job_id: UUID,
    format: str = Query("csv", pattern="^(csv|json)$"),
    db: Session = Depends(get_db)
):
    """
    Export ranked candidates as CSV.
    Conforms to TechSpec.md Section 3.7.
    """
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "code": "JOB_NOT_FOUND", "message": "Job not found."}
        )

    matches = db.query(JobMatch, Candidate).join(
        Candidate, JobMatch.candidate_id == Candidate.id
    ).filter(
        JobMatch.job_id == job_id
    ).order_by(
        JobMatch.rank.asc()
    ).all()

    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        
        # Write CSV Header
        writer.writerow([
            "Rank",
            "Filename",
            "Match Score (%)",
            "Matched Skills",
            "Missing Skills",
            "Extra Skills",
            "Years Experience",
            "Assessment"
        ])

        for match, cand in matches:
            writer.writerow([
                match.rank,
                cand.filename,
                f"{match.match_score:.1f}",
                ", ".join(match.matched_skills),
                ", ".join(match.missing_skills),
                ", ".join(match.extra_skills),
                cand.experience_years or 0,
                match.assessment
            ])

        csv_content = output.getvalue()
        output.close()

        safe_title = "".join([c if c.isalnum() else "_" for c in job.title])[:30]
        filename = f"candidates_ranking_{safe_title}_{str(job_id)[:8]}.csv"

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )

    # JSON export format
    data = []
    for match, cand in matches:
        data.append({
            "rank": match.rank,
            "filename": cand.filename,
            "match_score": match.match_score,
            "matched_skills": match.matched_skills,
            "missing_skills": match.missing_skills,
            "extra_skills": match.extra_skills,
            "years_experience": cand.experience_years,
            "assessment": match.assessment
        })

    return {
        "success": True,
        "data": {
            "job_id": str(job.id),
            "job_title": job.title,
            "candidates": data
        }
    }
