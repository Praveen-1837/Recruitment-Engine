export interface JobPosting {
  id: string;
  job_id?: string;
  title: string;
  description: string;
  extracted_requirements: {
    required_technical_skills?: string[];
    required_soft_skills?: string[];
    nice_to_have_skills?: string[];
    required_certifications?: string[];
    minimum_years_experience?: number;
    preferred_seniority_level?: string;
    required_languages?: string[];
    key_responsibilities?: string[];
  };
  required_years_experience?: number;
  seniority_level?: string;
  created_at: string;
  candidate_count?: number;
  is_analyzed?: boolean;
}

export interface CandidateUploaded {
  id: string;
  candidate_id?: string;
  job_id: string;
  filename: string;
  experience_years?: number;
  certification_count?: number;
  has_extracted_skills?: boolean;
  created_at: string;
}

export interface CandidateDetail {
  id: string;
  candidate_id: string;
  job_id: string;
  filename: string;
  extracted_skills: {
    technical_skills?: string[];
    soft_skills?: string[];
    certifications?: string[];
    languages?: string[];
    frameworks_libraries?: string[];
    tools?: string[];
    years_experience?: number;
    summary?: string;
  };
  experience_years?: number;
  certification_count?: number;
  text_preview?: string;
  created_at: string;
}

export interface CandidateMatch {
  candidate_id: string;
  filename: string;
  rank: number;
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  extra_skills: string[];
  matched_nice_to_have?: string[];
  experience_years?: number;
  experience_fit?: string;
  assessment: string;
}

export interface JobResultsData {
  job_id: string;
  job_title: string;
  job_description: string;
  extracted_requirements: any;
  total_candidates: number;
  best_match?: CandidateMatch;
  candidates: CandidateMatch[];
}

export interface CompareCandidateData {
  candidate_id: string;
  filename: string;
  rank?: number;
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  extra_skills: string[];
  years_experience: number;
}

export interface CompareResponseData {
  job_id: string;
  job_title: string;
  candidates: CompareCandidateData[];
  required_skills: string[];
  recommendation: string;
}
