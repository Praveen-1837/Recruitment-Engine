import json
import re
import time
import logging
from typing import Dict, Any, List, Optional
import anthropic
from config import settings

logger = logging.getLogger(__name__)

# Curated lists for robust NLP heuristic fallback
TECH_KEYWORDS = {
    "Python": ["python", "python3", "python 3"],
    "FastAPI": ["fastapi", "fast api"],
    "Django": ["django", "django rest framework", "drf"],
    "Flask": ["flask"],
    "PostgreSQL": ["postgresql", "postgres", "psql"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"],
    "Docker": ["docker", "containerization"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda", "ecs"],
    "GCP": ["gcp", "google cloud"],
    "Azure": ["azure", "microsoft azure"],
    "Git": ["git", "github", "gitlab"],
    "CI/CD": ["ci/cd", "continuous integration", "jenkins", "github actions"],
    "REST API": ["rest", "restful", "rest api", "apis"],
    "GraphQL": ["graphql"],
    "Linux": ["linux", "unix", "ubuntu"],
    "TypeScript": ["typescript", "ts"],
    "JavaScript": ["javascript", "js", "es6"],
    "React": ["react", "reactjs", "react.js"],
    "Node.js": ["nodejs", "node.js", "node"],
    "SQLAlchemy": ["sqlalchemy"],
    "Pandas": ["pandas", "numpy", "scipy"],
    "Kafka": ["kafka", "rabbitmq"],
    "Java": ["java", "spring", "spring boot"],
    "Go": ["golang", "go"],
    "C++": ["c++", "cpp"]
}

SOFT_KEYWORDS = {
    "Leadership": ["leadership", "led", "mentor", "managing", "management", "lead"],
    "Communication": ["communication", "presentation", "written", "verbal"],
    "Problem Solving": ["problem solving", "analytical", "troubleshooting", "critical thinking"],
    "Teamwork": ["teamwork", "collaboration", "cross-functional", "team player"],
    "Agile/Scrum": ["agile", "scrum", "kanban", "sprints"]
}

CERT_KEYWORDS = [
    "AWS Certified Solutions Architect",
    "AWS Certified Developer",
    "CKA (Certified Kubernetes Administrator)",
    "PMP",
    "Google Cloud Certified",
    "Azure Certified"
]

def clean_json_response(raw_text: str) -> str:
    """Strip markdown code fence blocks if Claude includes them."""
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def heuristic_extract_skills_from_resume(text: str) -> Dict[str, Any]:
    """Fallback NLP-based skill extraction from resume text."""
    lower_text = text.lower()
    
    found_tech = []
    found_frameworks = []
    found_tools = []
    
    for tech_name, aliases in TECH_KEYWORDS.items():
        for alias in aliases:
            # Word boundary search
            pattern = r"(?:\b|_)" + re.escape(alias) + r"(?:\b|_)"
            if re.search(pattern, lower_text):
                if tech_name in ["FastAPI", "Django", "Flask", "React", "SQLAlchemy"]:
                    found_frameworks.append(tech_name)
                elif tech_name in ["Docker", "Kubernetes", "Git", "CI/CD", "Linux"]:
                    found_tools.append(tech_name)
                else:
                    found_tech.append(tech_name)
                break
                
    found_soft = []
    for soft_name, aliases in SOFT_KEYWORDS.items():
        for alias in aliases:
            pattern = r"(?:\b|_)" + re.escape(alias) + r"(?:\b|_)"
            if re.search(pattern, lower_text):
                found_soft.append(soft_name)
                break
                
    found_certs = []
    for cert in CERT_KEYWORDS:
        if cert.lower() in lower_text:
            found_certs.append(cert)

    # Estimate years of experience
    exp_matches = re.findall(r"(\d{1,2})\+?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+experience)?", lower_text)
    years_exp = 0
    if exp_matches:
        try:
            ints = [int(m) for m in exp_matches if int(m) < 40]
            if ints:
                years_exp = max(ints)
        except Exception:
            years_exp = 0
            
    # Languages
    languages = ["English"]
    if "spanish" in lower_text:
        languages.append("Spanish")
    if "french" in lower_text:
        languages.append("French")
    if "german" in lower_text:
        languages.append("German")

    return {
        "technical_skills": sorted(list(set(found_tech))),
        "soft_skills": sorted(list(set(found_soft))),
        "certifications": found_certs,
        "languages": languages,
        "frameworks_libraries": sorted(list(set(found_frameworks))),
        "tools": sorted(list(set(found_tools))),
        "years_experience": years_exp,
        "summary": "Extracted qualifications via semantic resume parsing."
    }


def heuristic_extract_requirements_from_job(text: str) -> Dict[str, Any]:
    """Fallback NLP requirement extraction from job description text."""
    lower_text = text.lower()
    
    required_tech = []
    nice_to_have = []
    
    # Split text into sections if possible
    sections = re.split(r"(?:requirements|qualifications|nice to have|preferred|responsibilities)", lower_text)
    
    for tech_name, aliases in TECH_KEYWORDS.items():
        found = False
        for alias in aliases:
            pattern = r"(?:\b|_)" + re.escape(alias) + r"(?:\b|_)"
            if re.search(pattern, lower_text):
                found = True
                break
        if found:
            if "nice to have" in lower_text and any(alias in lower_text.split("nice to have")[-1] for alias in aliases):
                nice_to_have.append(tech_name)
            else:
                required_tech.append(tech_name)
                
    required_soft = []
    for soft_name, aliases in SOFT_KEYWORDS.items():
        for alias in aliases:
            pattern = r"(?:\b|_)" + re.escape(alias) + r"(?:\b|_)"
            if re.search(pattern, lower_text):
                required_soft.append(soft_name)
                break
                
    # Detect experience
    exp_matches = re.findall(r"(\d{1,2})\+?\s*(?:years?|yrs?)", lower_text)
    min_exp = 0
    if exp_matches:
        try:
            ints = [int(m) for m in exp_matches if int(m) < 40]
            if ints:
                min_exp = min(ints)
        except Exception:
            min_exp = 0

    # Detect seniority
    seniority = "mid-level"
    if "senior" in lower_text or "lead" in lower_text or "staff" in lower_text or min_exp >= 5:
        seniority = "senior"
    elif "junior" in lower_text or "entry" in lower_text or "intern" in lower_text or min_exp <= 2:
        seniority = "junior"

    return {
        "required_technical_skills": sorted(list(set(required_tech))),
        "required_soft_skills": sorted(list(set(required_soft))),
        "nice_to_have_skills": sorted(list(set(nice_to_have))),
        "required_certifications": [],
        "minimum_years_experience": min_exp,
        "preferred_seniority_level": seniority,
        "required_languages": ["English"],
        "key_responsibilities": ["Design and develop scalable applications", "Collaborate with cross-functional teams"]
    }


def call_claude_with_retry(system_prompt: str, user_prompt: str, max_retries: int = 3) -> Optional[str]:
    """Call Claude API with exponential backoff on errors."""
    if not settings.anthropic_api_key or settings.anthropic_api_key.strip() == "":
        logger.info("ANTHROPIC_API_KEY is not configured; using heuristic extraction.")
        return None

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    backoff = 1.0

    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model=settings.claude_model,
                max_tokens=1500,
                temperature=0.0,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return message.content[0].text
        except (anthropic.RateLimitError, anthropic.APIConnectionError) as e:
            logger.warning(f"Claude API transient error (attempt {attempt+1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                logger.error(f"Claude API exhausted retries: {e}")
                return None
            time.sleep(backoff)
            backoff *= 2.0
        except Exception as e:
            logger.error(f"Claude API non-retryable error: {e}")
            return None
    return None


def extract_skills_from_resume(resume_text: str) -> Dict[str, Any]:
    """Extract professional skills and attributes from resume text."""
    system_prompt = (
        "You are an expert recruiter analyzing resumes.\n"
        "Extract all professional skills from the provided resume.\n"
        "Focus on technical skills, soft skills, certifications, languages, frameworks, and tools.\n"
        "Return ONLY valid JSON, no markdown formatting, no explanations.\n"
        "Do not include generic filler phrases like 'hardworking' or 'punctual'.\n"
        "Be precise and extract exactly what is stated in the resume."
    )
    
    user_prompt = f"""Extract skills from this resume:

Resume Text:
{resume_text}

Return JSON with this exact structure (all fields required):
{{
  "technical_skills": ["skill1", "skill2"],
  "soft_skills": ["skill1", "skill2"],
  "certifications": ["cert1"],
  "languages": ["English", "Spanish"],
  "frameworks_libraries": ["framework1"],
  "tools": ["tool1"],
  "years_experience": 5,
  "summary": "Brief summary of qualifications"
}}"""

    response_text = call_claude_with_retry(system_prompt, user_prompt)
    if response_text:
        try:
            clean_str = clean_json_response(response_text)
            data = json.loads(clean_str)
            # Validate required fields
            for key in ["technical_skills", "soft_skills", "certifications", "languages", "frameworks_libraries", "tools"]:
                if key not in data or not isinstance(data[key], list):
                    data[key] = []
            if "years_experience" not in data:
                data["years_experience"] = 0
            if "summary" not in data:
                data["summary"] = ""
            return data
        except Exception as e:
            logger.error(f"Failed to parse Claude JSON response for resume: {e}. Falling back to heuristics.")

    return heuristic_extract_skills_from_resume(resume_text)


def extract_requirements_from_job(job_description: str) -> Dict[str, Any]:
    """Extract job requirements, technical skills, experience, and seniority from job description."""
    system_prompt = (
        "You are an expert HR analyst.\n"
        "Extract key requirements from job descriptions.\n"
        "Be precise and extract only explicitly stated requirements.\n"
        "Return ONLY valid JSON, no markdown, no conversational commentary."
    )
    
    user_prompt = f"""Extract requirements from this job posting:

Job Description:
{job_description}

Return JSON with this exact structure:
{{
  "required_technical_skills": ["Python", "FastAPI"],
  "required_soft_skills": ["Leadership"],
  "nice_to_have_skills": ["AWS"],
  "required_certifications": [],
  "minimum_years_experience": 5,
  "preferred_seniority_level": "mid-level",
  "required_languages": ["English"],
  "key_responsibilities": ["responsibility1"]
}}"""

    response_text = call_claude_with_retry(system_prompt, user_prompt)
    if response_text:
        try:
            clean_str = clean_json_response(response_text)
            data = json.loads(clean_str)
            for key in ["required_technical_skills", "required_soft_skills", "nice_to_have_skills", "required_certifications", "required_languages", "key_responsibilities"]:
                if key not in data or not isinstance(data[key], list):
                    data[key] = []
            if "minimum_years_experience" not in data:
                data["minimum_years_experience"] = 0
            if "preferred_seniority_level" not in data:
                data["preferred_seniority_level"] = "mid-level"
            return data
        except Exception as e:
            logger.error(f"Failed to parse Claude JSON response for job: {e}. Falling back to heuristics.")

    return heuristic_extract_requirements_from_job(job_description)
