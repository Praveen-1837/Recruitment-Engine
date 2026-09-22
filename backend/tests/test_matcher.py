import pytest
from services.matcher import calculate_match_score, normalize_skill

def test_normalize_skill():
    assert normalize_skill("  Python3  ") == "python"
    assert normalize_skill("Postgres") == "postgresql"
    assert normalize_skill("Fast API") == "fastapi"

def test_calculate_match_score_perfect():
    candidate_skills = {
        "technical_skills": ["Python", "PostgreSQL"],
        "frameworks_libraries": ["FastAPI"],
        "tools": ["Docker"],
        "soft_skills": ["Leadership"],
        "years_experience": 5
    }
    job_reqs = {
        "required_technical_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "required_soft_skills": ["Leadership"],
        "nice_to_have_skills": [],
        "minimum_years_experience": 5
    }
    result = calculate_match_score(candidate_skills, job_reqs)
    # Tech: 100 * 0.5 = 50, Exp: 100 * 0.3 = 30, Soft: 100 * 0.2 = 20, Penalties = 0 -> 100
    assert result["match_score"] == 100.0
    assert len(result["missing_skills"]) == 0
    assert result["experience_fit"] == "matches"

def test_calculate_match_score_penalties():
    candidate_skills = {
        "technical_skills": ["Python"],
        "frameworks_libraries": [],
        "tools": [],
        "soft_skills": [],
        "years_experience": 2
    }
    job_reqs = {
        "required_technical_skills": ["Python", "FastAPI", "PostgreSQL"],  # missing 2 skills
        "required_soft_skills": ["Leadership"],
        "nice_to_have_skills": ["AWS"],
        "minimum_years_experience": 4
    }
    result = calculate_match_score(candidate_skills, job_reqs)
    # Missing 2 tech skills: penalty = 2 * 10 = 20
    # Missing 1 nice-to-have: penalty = 1 * 2 = 2
    # Base score: tech: 1/3 * 50 = 16.7, exp: 2/4 * 30 = 15, soft: 0/1 * 20 = 0 -> base = 31.7
    # Penalties: 22 -> 31.7 - 22 = 9.7
    assert result["match_score"] < 20.0
    assert len(result["missing_skills"]) == 2
    assert "FastAPI" in result["missing_skills"]
    assert "PostgreSQL" in result["missing_skills"]
    assert result["experience_fit"] == "below"
