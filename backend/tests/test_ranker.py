import uuid
import pytest
from services.ranker import rank_candidates, generate_comparison_recommendation

def test_rank_candidates_sorting():
    c1_id = uuid.uuid4()
    c2_id = uuid.uuid4()
    c3_id = uuid.uuid4()

    candidates = [
        {
            "candidate": {"id": c1_id, "filename": "mid.pdf"},
            "match_details": {
                "match_score": 75.0,
                "matched_skills": ["Python", "FastAPI"],
                "missing_skills": ["AWS"],
                "extra_skills": [],
                "matched_nice_to_have": [],
                "candidate_years_experience": 4,
                "experience_fit": "matches"
            }
        },
        {
            "candidate": {"id": c2_id, "filename": "top.pdf"},
            "match_details": {
                "match_score": 92.0,
                "matched_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "missing_skills": [],
                "extra_skills": ["Git"],
                "matched_nice_to_have": [],
                "candidate_years_experience": 6,
                "experience_fit": "exceeds"
            }
        },
        {
            "candidate": {"id": c3_id, "filename": "low.pdf"},
            "match_details": {
                "match_score": 40.0,
                "matched_skills": ["Python"],
                "missing_skills": ["FastAPI", "PostgreSQL"],
                "extra_skills": [],
                "matched_nice_to_have": [],
                "candidate_years_experience": 1,
                "experience_fit": "below"
            }
        }
    ]

    ranked = rank_candidates(candidates)
    assert len(ranked) == 3
    assert ranked[0]["candidate_id"] == c2_id
    assert ranked[0]["rank"] == 1
    assert ranked[0]["match_score"] == 92.0

    assert ranked[1]["candidate_id"] == c1_id
    assert ranked[1]["rank"] == 2

    assert ranked[2]["candidate_id"] == c3_id
    assert ranked[2]["rank"] == 3

def test_generate_comparison_recommendation():
    candidates = [
        {"filename": "alex.pdf", "match_score": 90.0},
        {"filename": "jordan.pdf", "match_score": 60.0}
    ]
    rec = generate_comparison_recommendation(candidates, "Python Engineer")
    assert "alex.pdf" in rec
    assert "distinctly stronger" in rec
