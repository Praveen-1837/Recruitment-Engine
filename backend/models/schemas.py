from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

# Base Generic API Responses
class BaseSuccessResponse(BaseModel):
    success: bool = True
    data: Any
    message: Optional[str] = None

class ErrorDetail(BaseModel):
    error: bool = True
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


# Job Schemas
class JobCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=255, description="Job title")
    description: str = Field(..., min_length=20, max_length=50000, description="Full job description")

class JobExtractedRequirements(BaseModel):
    required_technical_skills: List[str] = Field(default_factory=list)
    required_soft_skills: List[str] = Field(default_factory=list)
    nice_to_have_skills: List[str] = Field(default_factory=list)
    required_certifications: List[str] = Field(default_factory=list)
    minimum_years_experience: int = 0
    preferred_seniority_level: str = "mid-level"
    required_languages: List[str] = Field(default_factory=list)
    key_responsibilities: List[str] = Field(default_factory=list)

class JobResponseData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    extracted_requirements: Dict[str, Any]
    required_years_experience: Optional[int] = None
    seniority_level: Optional[str] = None
    created_at: datetime
    candidate_count: Optional[int] = 0
    is_analyzed: Optional[bool] = False


# Candidate Upload Schemas
class UploadedFileInfo(BaseModel):
    filename: str
    candidate_id: UUID
    size_bytes: int

class UploadResponseData(BaseModel):
    job_id: UUID
    uploaded_files: List[UploadedFileInfo]
    total_uploaded: int
    failed: int = 0
    errors: List[str] = Field(default_factory=list)


# Candidate Schemas
class ExtractedSkillsSchema(BaseModel):
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    frameworks_libraries: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    years_experience: int = 0
    summary: str = ""

class CandidateSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    job_id: UUID
    filename: str
    experience_years: Optional[int] = 0
    certification_count: Optional[int] = 0
    extracted_skills: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

class CandidateDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    job_id: UUID
    filename: str
    original_text: str
    extracted_skills: Dict[str, Any]
    experience_years: Optional[int] = 0
    certification_count: Optional[int] = 0
    created_at: datetime


# Analysis & Match Schemas
class CandidateRankedResult(BaseModel):
    candidate_id: UUID
    filename: str
    rank: int
    match_score: float
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    extra_skills: List[str] = Field(default_factory=list)
    matched_nice_to_have: List[str] = Field(default_factory=list)
    experience_years: Optional[int] = 0
    experience_fit: Optional[str] = "matches"
    assessment: str = ""

class AnalyzeResponseData(BaseModel):
    job_id: UUID
    candidates_ranked: List[CandidateRankedResult]
    analysis_completed_at: str
    top_match: Optional[Dict[str, Any]] = None


# Compare Schemas
class CompareRequest(BaseModel):
    job_id: UUID
    candidate_ids: List[UUID]

class CompareCandidateData(BaseModel):
    candidate_id: UUID
    filename: str
    rank: Optional[int] = None
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    extra_skills: List[str]
    years_experience: int

class CompareResponseData(BaseModel):
    job_id: UUID
    job_title: str
    candidates: List[CompareCandidateData]
    required_skills: List[str]
    recommendation: str
