from typing import Dict, Any, List, Set

def normalize_skill(skill: str) -> str:
    """Normalize skill string for case-insensitive matching."""
    s = skill.strip().lower()
    # Canonical mappings for common synonyms
    synonyms = {
        "python3": "python",
        "py": "python",
        "postgres": "postgresql",
        "psql": "postgresql",
        "react.js": "react",
        "reactjs": "react",
        "node": "node.js",
        "nodejs": "node.js",
        "k8s": "kubernetes",
        "fast api": "fastapi",
        "drf": "django",
        "amazon web services": "aws",
        "gcp": "google cloud",
        "ci cd": "ci/cd"
    }
    return synonyms.get(s, s)

def calculate_match_score(candidate_skills: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate comprehensive match score and breakdown for candidate-job pair.
    Adheres strictly to TechSpec.md Section 7 and Memory.md Section 8.
    """
    # Aggregate all candidate technical skills (from technical, frameworks, and tools)
    raw_cand_tech = (
        candidate_skills.get("technical_skills", []) +
        candidate_skills.get("frameworks_libraries", []) +
        candidate_skills.get("tools", [])
    )
    raw_cand_soft = candidate_skills.get("soft_skills", [])
    cand_exp = candidate_skills.get("years_experience", 0) or 0

    # Job requirements
    raw_req_tech = job_requirements.get("required_technical_skills", [])
    raw_req_soft = job_requirements.get("required_soft_skills", [])
    raw_nice_to_have = job_requirements.get("nice_to_have_skills", [])
    req_exp = job_requirements.get("minimum_years_experience", 0) or 0

    # Create mapping of normalized -> original display name
    cand_tech_map = {normalize_skill(s): s for s in raw_cand_tech}
    cand_soft_map = {normalize_skill(s): s for s in raw_cand_soft}
    
    req_tech_map = {normalize_skill(s): s for s in raw_req_tech}
    req_soft_map = {normalize_skill(s): s for s in raw_req_soft}
    nice_map = {normalize_skill(s): s for s in raw_nice_to_have}

    norm_cand_tech = set(cand_tech_map.keys())
    norm_cand_soft = set(cand_soft_map.keys())
    norm_req_tech = set(req_tech_map.keys())
    norm_req_soft = set(req_soft_map.keys())
    norm_nice = set(nice_map.keys())

    # Matches
    matched_tech_keys = norm_cand_tech & norm_req_tech
    matched_soft_keys = norm_cand_soft & norm_req_soft
    matched_nice_keys = norm_cand_tech & norm_nice

    missing_tech_keys = norm_req_tech - norm_cand_tech
    missing_nice_keys = norm_nice - norm_cand_tech
    extra_tech_keys = norm_cand_tech - norm_req_tech - norm_nice

    # Format output lists with nice capitalization
    matched_skills = [req_tech_map.get(k, cand_tech_map.get(k, k.capitalize())) for k in matched_tech_keys] + \
                     [req_soft_map.get(k, cand_soft_map.get(k, k.capitalize())) for k in matched_soft_keys]
    missing_skills = [req_tech_map[k] for k in missing_tech_keys]
    extra_skills = [cand_tech_map[k] for k in extra_tech_keys]
    matched_nice_to_have = [nice_map[k] for k in matched_nice_keys]

    # Technical Match (0 - 100)
    if len(norm_req_tech) > 0:
        tech_match = (len(matched_tech_keys) / len(norm_req_tech)) * 100.0
    else:
        tech_match = 100.0

    # Experience Match (0 - 100)
    if req_exp > 0:
        exp_match = min(cand_exp / req_exp, 1.0) * 100.0
    else:
        exp_match = 100.0

    # Soft Skills Match (0 - 100)
    if len(norm_req_soft) > 0:
        soft_match = (len(matched_soft_keys) / len(norm_req_soft)) * 100.0
    else:
        soft_match = 100.0

    # Overall base score (0.5 tech + 0.3 exp + 0.2 soft)
    overall_score = (tech_match * 0.5) + (exp_match * 0.3) + (soft_match * 0.2)

    # Penalties
    # Critical missing skills: -10 points each
    # Missing nice-to-have: -2 points each
    penalties = (len(missing_tech_keys) * 10.0) + (len(missing_nice_keys) * 2.0)
    
    # Final score capped between 0 and 100
    final_score = max(0.0, min(100.0, overall_score - penalties))

    # Experience fit assessment
    if req_exp > 0:
        if cand_exp > req_exp:
            exp_fit = "exceeds"
        elif cand_exp == req_exp:
            exp_fit = "matches"
        else:
            exp_fit = "below"
    else:
        exp_fit = "matches"

    return {
        "match_score": round(final_score, 1),
        "tech_match": round(tech_match, 1),
        "exp_match": round(exp_match, 1),
        "soft_match": round(soft_match, 1),
        "matched_skills": sorted(list(set(matched_skills))),
        "missing_skills": sorted(list(set(missing_skills))),
        "extra_skills": sorted(list(set(extra_skills))),
        "matched_nice_to_have": sorted(list(set(matched_nice_to_have))),
        "experience_fit": exp_fit,
        "candidate_years_experience": cand_exp,
        "required_years_experience": req_exp
    }
