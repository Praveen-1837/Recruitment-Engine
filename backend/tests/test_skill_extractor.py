import pytest
from services.skill_extractor import (
    clean_json_response,
    heuristic_extract_skills_from_resume,
    heuristic_extract_requirements_from_job,
    extract_skills_from_resume,
    extract_requirements_from_job
)

def test_clean_json_response():
    markdown_wrapped = '```json\n{"key": "value"}\n```'
    cleaned = clean_json_response(markdown_wrapped)
    assert cleaned == '{"key": "value"}'

def test_heuristic_extract_skills():
    resume_sample = """
    John Doe - Senior Software Engineer
    Over 6 years of experience building applications in Python, FastAPI, and PostgreSQL.
    Proficient with Docker, Kubernetes, and AWS cloud infrastructure.
    Strong leadership and agile team communication.
    """
    skills = heuristic_extract_skills_from_resume(resume_sample)
    assert "Python" in skills["technical_skills"]
    assert "FastAPI" in skills["frameworks_libraries"]
    assert "PostgreSQL" in skills["technical_skills"]
    assert "Docker" in skills["tools"]
    assert "AWS" in skills["technical_skills"]
    assert skills["years_experience"] == 6

def test_heuristic_extract_requirements():
    job_desc = """
    We are seeking a Senior Python Developer with at least 5 years of experience.
    Must have extensive knowledge of Python, FastAPI, and PostgreSQL.
    Experience with Docker and AWS is nice to have.
    Requires strong communication and problem solving skills.
    """
    reqs = heuristic_extract_requirements_from_job(job_desc)
    assert "Python" in reqs["required_technical_skills"]
    assert "FastAPI" in reqs["required_technical_skills"]
    assert reqs["minimum_years_experience"] == 5
    assert reqs["preferred_seniority_level"] == "senior"

def test_extract_skills_wrapper():
    # Calling wrapper should return valid dictionary
    text = "Developer with 3 years experience in Django and Git."
    res = extract_skills_from_resume(text)
    assert isinstance(res, dict)
    assert "Django" in res["frameworks_libraries"] or "Django" in res["technical_skills"]
