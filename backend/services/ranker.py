from typing import List, Dict, Any

def generate_assessment_text(candidate_data: Dict[str, Any], match_details: Dict[str, Any]) -> str:
    """Generate concise recruiter-facing assessment summary."""
    score = match_details["match_score"]
    matched = match_details["matched_skills"]
    missing = match_details["missing_skills"]
    exp_fit = match_details["experience_fit"]
    cand_exp = match_details["candidate_years_experience"]

    matched_sample = ", ".join(matched[:3]) if matched else "none"
    missing_sample = ", ".join(missing[:3]) if missing else "none"

    if score >= 90:
        return (
            f"Top-tier match ({score}%). Possesses core required competencies including {matched_sample}. "
            f"Experience ({cand_exp} yrs) {exp_fit} requirements. Immediate high-priority interview recommendation."
        )
    elif score >= 75:
        return (
            f"Strong contender ({score}%). Solid foundation in {matched_sample}. "
            f"{'Minor skill gap in ' + missing_sample + '.' if missing else 'Well-rounded profile.'} "
            f"Viable candidate ready to contribute."
        )
    elif score >= 50:
        return (
            f"Moderate fit ({score}%). Possesses some relevant skills ({matched_sample}), "
            f"but missing critical prerequisites ({missing_sample}). May require onboarding ramp-up."
        )
    else:
        return (
            f"Low alignment ({score}%). Lacks multiple required competencies ({missing_sample}). "
            f"Does not currently satisfy minimum qualification thresholds for this role."
        )

def rank_candidates(candidates_match_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort candidates by match_score DESC, matched skills count DESC, years_experience DESC,
    and assign integer rank (1-indexed).
    """
    sorted_candidates = sorted(
        candidates_match_list,
        key=lambda c: (
            c["match_details"]["match_score"],
            len(c["match_details"]["matched_skills"]),
            c["match_details"].get("candidate_years_experience", 0)
        ),
        reverse=True
    )

    ranked_results = []
    for idx, item in enumerate(sorted_candidates, start=1):
        assessment = generate_assessment_text(item["candidate"], item["match_details"])
        ranked_results.append({
            "candidate_id": item["candidate"]["id"],
            "filename": item["candidate"]["filename"],
            "rank": idx,
            "match_score": item["match_details"]["match_score"],
            "matched_skills": item["match_details"]["matched_skills"],
            "missing_skills": item["match_details"]["missing_skills"],
            "extra_skills": item["match_details"]["extra_skills"],
            "matched_nice_to_have": item["match_details"]["matched_nice_to_have"],
            "experience_years": item["match_details"]["candidate_years_experience"],
            "experience_fit": item["match_details"]["experience_fit"],
            "assessment": assessment
        })

    return ranked_results


def generate_comparison_recommendation(candidates: List[Dict[str, Any]], job_title: str) -> str:
    """Generate executive summary comparing 2-3 candidates."""
    if not candidates:
        return "No candidates provided for comparison."

    sorted_candidates = sorted(candidates, key=lambda c: c["match_score"], reverse=True)
    top = sorted_candidates[0]

    if len(candidates) == 1:
        return f"{top['filename']} has a match score of {top['match_score']}% for the {job_title} role."

    second = sorted_candidates[1]
    diff = round(top["match_score"] - second["match_score"], 1)

    if diff >= 15:
        rec = (
            f"{top['filename']} is the distinctly stronger candidate for {job_title} ({top['match_score']}% vs {second['match_score']}%). "
            f"They possess a broader alignment with core required technologies and demonstrated relevant experience."
        )
    elif diff >= 5:
        rec = (
            f"{top['filename']} holds a moderate advantage ({top['match_score']}%) over {second['filename']} ({second['match_score']}%). "
            f"Both candidates bring valuable capabilities, with {top['filename']} presenting fewer missing technical requirements."
        )
    else:
        rec = (
            f"{top['filename']} ({top['match_score']}%) and {second['filename']} ({second['match_score']}%) are closely matched. "
            f"The final decision should weigh specific domain depth and team culture interview signals."
        )

    return rec
