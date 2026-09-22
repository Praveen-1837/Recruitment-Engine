# TechSpec.md
## Technical Specifications - Recruitment Intelligence Engine

---

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│  Next.js (TypeScript) - UI, Upload, Results, Comparison     │
│  Port: 3000                                                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
                    HTTP/REST API
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Backend Layer                             │
│  FastAPI (Python) - Business Logic, AI Integration          │
│  Port: 8000                                                 │
│  ├── File Processing Service                               │
│  ├── Skill Extraction Service (Claude)                      │
│  ├── Matching & Ranking Service                             │
│  └── Database Layer (SQLAlchemy ORM)                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    PostgreSQL        Claude API        File Storage
    (Port 5432)       (API Calls)         (Local/S3)
```

---

## 2. Technology Stack Details

### 2.1 Frontend

**Stack:**
- Framework: Next.js 14.0+
- Language: TypeScript 5+
- UI/Styling: Tailwind CSS 3+
- State Management: React Context API
- HTTP Client: axios or fetch API
- Build Tool: webpack (via Next.js)
- Node.js: 18.17+ or 20+

**Dependencies:**
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "axios": "^1.6.0",
    "tailwindcss": "^3.3.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/node": "^20.0.0",
    "jest": "^29.0.0",
    "@testing-library/react": "^14.0.0",
    "eslint": "^8.0.0"
  }
}
```

**File Structure:**
```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home page
│   ├── upload/
│   │   └── page.tsx         # Upload interface
│   ├── results/
│   │   └── [jobId]/page.tsx # Results page
│   ├── compare/
│   │   └── page.tsx         # Comparison view
│   └── api/                 # Client-side API calls
├── components/
│   ├── ResumeUploader.tsx
│   ├── JobDescriptionInput.tsx
│   ├── CandidateCard.tsx
│   ├── CandidateList.tsx
│   ├── ComparisonTable.tsx
│   ├── SkillBadge.tsx
│   └── LoadingSpinner.tsx
├── lib/
│   ├── api.ts               # API client functions
│   ├── types.ts             # TypeScript interfaces
│   └── utils.ts             # Utility functions
├── styles/
│   └── globals.css
├── public/
│   └── (assets)
├── .env.local               # Environment variables
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
└── package.json
```

### 2.2 Backend

**Stack:**
- Framework: FastAPI 0.104+
- Language: Python 3.10+
- Web Server: Uvicorn
- ORM: SQLAlchemy 2.0+
- Database Driver: psycopg2-binary
- Async: asyncio + aiofiles
- File Processing: PyPDF2, python-docx, pytesseract (OCR)
- LLM Client: anthropic SDK

**Dependencies:**
```
fastapi==0.104.0
uvicorn==0.24.0
sqlalchemy==2.0.0
psycopg2-binary==2.9.0
python-dotenv==1.0.0
pydantic==2.0.0
pydantic-settings==2.0.0
anthropic==0.13.0
PyPDF2==3.0.0
python-docx==0.8.11
pytesseract==0.3.10
aiofiles==23.0.0
python-multipart==0.0.6
```

**File Structure:**
```
backend/
├── main.py                  # FastAPI app entry point
├── config.py                # Configuration, env vars
├── requirements.txt         # Python dependencies
├── routes/
│   ├── __init__.py
│   ├── health.py           # Health check endpoint
│   ├── upload.py           # Resume upload endpoints
│   ├── analyze.py          # Analysis endpoints
│   └── results.py          # Results retrieval
├── services/
│   ├── __init__.py
│   ├── file_processor.py    # Extract text from files
│   ├── skill_extractor.py   # Claude skill extraction
│   ├── matcher.py           # Skill matching logic
│   └── ranker.py            # Ranking algorithm
├── models/
│   ├── __init__.py
│   ├── database.py          # SQLAlchemy models
│   └── schemas.py           # Pydantic schemas
├── utils/
│   ├── __init__.py
│   ├── claude_client.py      # Claude API wrapper
│   └── validators.py         # Input validation
├── tests/
│   ├── test_file_processor.py
│   ├── test_skill_extractor.py
│   ├── test_matcher.py
│   └── test_ranker.py
├── .env                      # Environment variables
├── .env.example              # Template
├── docker-compose.yml        # PostgreSQL + backend
└── Dockerfile                # Container image
```

### 2.3 Database

**Type:** PostgreSQL 14+

**Schemas:**
```sql
-- Candidates table
CREATE TABLE candidates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES job_postings(id),
    filename VARCHAR(255) NOT NULL,
    original_text TEXT NOT NULL,
    extracted_skills JSONB NOT NULL,
    experience_years INTEGER,
    certification_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job postings table
CREATE TABLE job_postings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    extracted_requirements JSONB NOT NULL,
    required_years_experience INTEGER,
    seniority_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analysis results table
CREATE TABLE job_matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    job_id UUID NOT NULL REFERENCES job_postings(id),
    match_score FLOAT NOT NULL,
    matched_skills JSONB NOT NULL,
    missing_skills JSONB NOT NULL,
    extra_skills JSONB NOT NULL,
    assessment TEXT,
    rank INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indices for performance
CREATE INDEX idx_candidates_job_id ON candidates(job_id);
CREATE INDEX idx_job_matches_candidate_id ON job_matches(candidate_id);
CREATE INDEX idx_job_matches_job_id ON job_matches(job_id);
CREATE INDEX idx_job_matches_score ON job_matches(match_score DESC);
```

---

## 3. API Specifications

### 3.1 Health Check
```
GET /health
Response: 200
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-09-22T10:30:00Z"
}
```

### 3.2 Upload Resumes
```
POST /api/upload
Content-Type: multipart/form-data

Request:
- files: File[] (PDF, DOCX, TXT)
- job_id: string (UUID)

Response: 201
{
  "success": true,
  "data": {
    "job_id": "uuid",
    "uploaded_files": [
      {
        "filename": "resume.pdf",
        "candidate_id": "uuid",
        "size_bytes": 1024
      }
    ],
    "total_uploaded": 5
  }
}

Error: 400 / 413
{
  "error": true,
  "code": "INVALID_FILE_TYPE",
  "message": "Only PDF, DOCX, and TXT files are supported"
}
```

### 3.3 Create Job Posting
```
POST /api/jobs
Content-Type: application/json

Request:
{
  "title": "Python Developer",
  "description": "We are looking for... (full job description)"
}

Response: 201
{
  "success": true,
  "data": {
    "job_id": "uuid",
    "title": "Python Developer",
    "requirements_extracted": true,
    "required_skills": [
      "Python",
      "FastAPI",
      "PostgreSQL"
    ]
  }
}
```

### 3.4 Analyze & Rank Candidates
```
POST /api/analyze/{job_id}
Content-Type: application/json

Request:
{
  "job_id": "uuid"
}

Response: 200
{
  "success": true,
  "data": {
    "job_id": "uuid",
    "candidates_ranked": [
      {
        "candidate_id": "uuid",
        "filename": "john_doe.pdf",
        "rank": 1,
        "match_score": 92,
        "matched_skills": ["Python", "FastAPI"],
        "missing_skills": ["AWS"],
        "extra_skills": ["Docker"],
        "assessment": "Strong match, has all core requirements"
      },
      {
        "candidate_id": "uuid",
        "filename": "jane_smith.pdf",
        "rank": 2,
        "match_score": 78,
        "matched_skills": ["Python", "PostgreSQL"],
        "missing_skills": ["FastAPI", "AWS"],
        "extra_skills": []
      }
    ],
    "analysis_completed_at": "2026-09-22T10:35:00Z"
  }
}
```

### 3.5 Get Candidate Details
```
GET /api/candidates/{candidate_id}

Response: 200
{
  "success": true,
  "data": {
    "candidate_id": "uuid",
    "filename": "john_doe.pdf",
    "extracted_skills": {
      "technical": ["Python", "FastAPI", "PostgreSQL"],
      "soft": ["Leadership", "Communication"],
      "certifications": ["AWS Solutions Architect"],
      "languages": ["English", "Spanish"]
    },
    "experience_years": 5,
    "education": ["BS Computer Science"]
  }
}
```

### 3.6 Compare Candidates
```
POST /api/compare
Content-Type: application/json

Request:
{
  "candidate_ids": ["uuid1", "uuid2"],
  "job_id": "uuid"
}

Response: 200
{
  "success": true,
  "data": {
    "candidates": [
      {
        "candidate_id": "uuid1",
        "filename": "john.pdf",
        "match_score": 92,
        "matched_skills": ["Python", "FastAPI"],
        "missing_skills": ["AWS"],
        "years_experience": 5
      },
      {
        "candidate_id": "uuid2",
        "filename": "jane.pdf",
        "match_score": 78,
        "matched_skills": ["Python", "PostgreSQL"],
        "missing_skills": ["FastAPI", "AWS"],
        "years_experience": 3
      }
    ],
    "recommendation": "Candidate 1 is a stronger match"
  }
}
```

### 3.7 Export Results
```
GET /api/export/{job_id}?format=csv

Response: 200
Content-Type: text/csv

rank,name,filename,match_score,matched_skills,missing_skills
1,John Doe,john.pdf,92,"Python, FastAPI","AWS"
2,Jane Smith,jane.pdf,78,"Python, PostgreSQL","FastAPI, AWS"
```

---

## 4. Data Models & Schemas

### 4.1 Candidate Model
```python
class Candidate(Base):
    __tablename__ = "candidates"
    
    id: UUID = Column(Uuid, primary_key=True, default=uuid4)
    job_id: UUID = Column(Uuid, ForeignKey("job_postings.id"), nullable=False)
    filename: str = Column(String(255), nullable=False)
    original_text: str = Column(Text, nullable=False)
    extracted_skills: dict = Column(JSON, nullable=False)
    experience_years: Optional[int] = Column(Integer)
    certification_count: int = Column(Integer, default=0)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CandidateSchema(BaseModel):
    id: UUID
    filename: str
    extracted_skills: dict
    experience_years: Optional[int]
    certification_count: int
```

### 4.2 Job Posting Model
```python
class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id: UUID = Column(Uuid, primary_key=True, default=uuid4)
    title: str = Column(String(255), nullable=False)
    description: str = Column(Text, nullable=False)
    extracted_requirements: dict = Column(JSON, nullable=False)
    required_years_experience: Optional[int] = Column(Integer)
    seniority_level: Optional[str] = Column(String(50))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

class JobPostingSchema(BaseModel):
    title: str
    description: str
    extracted_requirements: Optional[dict] = None
    required_years_experience: Optional[int] = None
```

### 4.3 Job Match Model
```python
class JobMatch(Base):
    __tablename__ = "job_matches"
    
    id: UUID = Column(Uuid, primary_key=True, default=uuid4)
    candidate_id: UUID = Column(Uuid, ForeignKey("candidates.id"), nullable=False)
    job_id: UUID = Column(Uuid, ForeignKey("job_postings.id"), nullable=False)
    match_score: float = Column(Float, nullable=False)
    matched_skills: list = Column(JSON, nullable=False)
    missing_skills: list = Column(JSON, nullable=False)
    extra_skills: list = Column(JSON, nullable=False)
    assessment: str = Column(Text, nullable=False)
    rank: int = Column(Integer, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
```

---

## 5. Claude Integration

### 5.1 Skill Extraction Prompt

**System:**
```
You are an expert recruiter analyzing resumes.
Extract all professional skills from the provided resume.
Focus on technical skills, soft skills, certifications, languages, and frameworks.
Return ONLY valid JSON, no markdown, no explanations.
Do not include generic phrases like "hardworking" or "punctual".
Be precise and extract exactly what is stated in the resume.
```

**User Prompt Template:**
```
Extract skills from this resume:

Resume Text:
{resume_text}

Return JSON with this exact structure (all fields required):
{
  "technical_skills": ["skill1", "skill2"],
  "soft_skills": ["skill1", "skill2"],
  "certifications": ["cert1"],
  "languages": ["English", "Spanish"],
  "frameworks_libraries": ["framework1"],
  "tools": ["tool1"],
  "years_experience": 5,
  "summary": "Brief summary of key qualifications"
}
```

### 5.2 Job Requirement Extraction Prompt

**System:**
```
You are an expert HR analyst.
Extract key requirements from job descriptions.
Be precise and extract only explicitly stated requirements.
Return ONLY valid JSON, no markdown.
```

**User Prompt Template:**
```
Extract requirements from this job posting:

Job Description:
{job_description}

Return JSON with this exact structure:
{
  "required_technical_skills": ["Python", "FastAPI"],
  "required_soft_skills": ["Leadership"],
  "nice_to_have_skills": ["AWS"],
  "required_certifications": [],
  "minimum_years_experience": 5,
  "preferred_seniority_level": "mid-level",
  "required_languages": ["English"],
  "key_responsibilities": ["responsibility1"]
}
```

### 5.3 Matching & Scoring Prompt

**System:**
```
You are an expert in evaluating candidate-job fit.
Compare candidate skills to job requirements.
Be objective and precise in your assessment.
Return ONLY valid JSON, no markdown.
```

**User Prompt Template:**
```
Evaluate this candidate's match for the job:

Candidate Skills:
{candidate_skills_json}

Job Requirements:
{job_requirements_json}

Return JSON with this structure:
{
  "match_score": 85,
  "matched_skills": ["skill1", "skill2"],
  "missing_critical_skills": ["skill1"],
  "missing_nice_to_have": ["skill1"],
  "extra_skills": ["skill1"],
  "experience_fit": "exceeds requirements",
  "brief_assessment": "Strong match with all core skills",
  "recommendations": ["recommendation1"]
}
```

### 5.4 Claude API Call Example

```python
import anthropic
import json

def extract_skills_from_resume(resume_text: str) -> dict:
    client = anthropic.Anthropic()
    
    try:
        message = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": f"""Extract skills from this resume:

Resume Text:
{resume_text}

Return JSON with this exact structure (all fields required):
{{
  "technical_skills": ["skill1", "skill2"],
  "soft_skills": ["skill1"],
  "certifications": ["cert1"],
  "languages": ["English"],
  "frameworks_libraries": ["framework1"],
  "tools": ["tool1"],
  "years_experience": 5,
  "summary": "Brief summary"
}}"""
                }
            ]
        )
        
        response_text = message.content[0].text
        skills_data = json.loads(response_text)
        return skills_data
        
    except anthropic.APIError as e:
        logger.error(f"Claude API error: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response: {str(e)}")
        raise
```

---

## 6. File Processing Pipeline

### 6.1 Supported Formats

| Format | MIME Type | Library | Max Size |
|--------|-----------|---------|----------|
| PDF | application/pdf | PyPDF2 | 10 MB |
| DOCX | application/vnd.openxmlformats-officedocument.wordprocessingml.document | python-docx | 10 MB |
| TXT | text/plain | Built-in | 10 MB |

### 6.2 Processing Pipeline

```
1. File Upload
   ├── Validate MIME type
   ├── Check file size (< 10MB)
   └── Store temporarily

2. Text Extraction
   ├── PDF → PyPDF2 extraction
   │   └── If scanned → Tesseract OCR
   ├── DOCX → python-docx
   └── TXT → Read directly

3. Text Cleaning
   ├── Remove extra whitespace
   ├── Remove special characters
   ├── Normalize line breaks
   └── Validate text length

4. Skill Extraction
   ├── Call Claude API
   ├── Parse JSON response
   └── Store in database

5. Cleanup
   ├── Delete temporary file
   └── Keep extracted data only
```

### 6.3 Implementation

```python
import PyPDF2
from docx import Document
import pytesseract
from PIL import Image
import os

async def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF, DOCX, or TXT file"""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            return extract_text_from_docx(file_path)
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    except Exception as e:
        logger.error(f"Error extracting text: {str(e)}")
        raise

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using PyPDF2 with fallback to OCR"""
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            
            # If PyPDF2 couldn't extract text (scanned PDF), use OCR
            if not page_text or len(page_text.strip()) < 50:
                page_text = perform_ocr(file_path, page_num)
            
            text += page_text + "\n"
    
    return text.strip()

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text.strip()

def perform_ocr(file_path: str, page_num: int) -> str:
    """Use Tesseract OCR for scanned PDFs"""
    # Convert PDF page to image and run OCR
    from pdf2image import convert_from_path
    
    try:
        images = convert_from_path(file_path, first_page=page_num+1, last_page=page_num+1)
        if images:
            text = pytesseract.image_to_string(images[0])
            return text
    except Exception as e:
        logger.error(f"OCR failed: {str(e)}")
    
    return ""
```

---

## 7. Ranking Algorithm

### 7.1 Scoring Methodology

```
Overall Match Score = (Technical Match × 0.5) + (Experience Match × 0.3) + (Soft Skills Match × 0.2)

Technical Match = (Matched Technical Skills / Required Technical Skills) × 100
Experience Match = min(Candidate Years / Required Years, 1.0) × 100
Soft Skills Match = (Matched Soft Skills / Required Soft Skills) × 100

Penalties:
- Missing critical skill: -10 points each
- Missing nice-to-have: -2 points each
```

### 7.2 Python Implementation

```python
def calculate_match_score(candidate: dict, job: dict) -> dict:
    """
    Calculate comprehensive match score for candidate-job pair
    """
    # Extract skills
    candidate_tech = set(candidate['extracted_skills'].get('technical_skills', []))
    candidate_soft = set(candidate['extracted_skills'].get('soft_skills', []))
    candidate_exp = candidate['extracted_skills'].get('years_experience', 0)
    
    required_tech = set(job['extracted_requirements'].get('required_technical_skills', []))
    required_soft = set(job['extracted_requirements'].get('required_soft_skills', []))
    required_exp = job['extracted_requirements'].get('minimum_years_experience', 0)
    nice_to_have = set(job['extracted_requirements'].get('nice_to_have_skills', []))
    
    # Calculate matches
    matched_tech = candidate_tech & required_tech
    matched_soft = candidate_soft & required_soft
    matched_nice = candidate_tech & nice_to_have
    missing_tech = required_tech - candidate_tech
    
    # Technical match score
    tech_match = len(matched_tech) / len(required_tech) * 100 if required_tech else 100
    
    # Experience match score
    exp_match = min(candidate_exp / max(required_exp, 1), 1.0) * 100
    
    # Soft skills match score
    soft_match = len(matched_soft) / len(required_soft) * 100 if required_soft else 100
    
    # Overall score
    overall_score = (tech_match * 0.5) + (exp_match * 0.3) + (soft_match * 0.2)
    
    # Penalties
    penalties = len(missing_tech) * 10  # Critical skill penalty
    overall_score = max(0, overall_score - penalties)
    
    return {
        "match_score": round(overall_score),
        "matched_skills": list(matched_tech | matched_soft),
        "missing_skills": list(missing_tech),
        "extra_skills": list(candidate_tech - required_tech - nice_to_have),
        "matched_nice_to_have": list(matched_nice),
        "experience_fit": "exceeds" if candidate_exp > required_exp else ("matches" if candidate_exp >= required_exp else "below")
    }
```

---

## 8. Performance Benchmarks

| Operation | Target | Method |
|-----------|--------|--------|
| File upload | <5s | Async upload, streaming |
| Resume parsing | <10s per file | Parallel processing |
| Skill extraction | <30s per resume | Claude API with caching |
| Matching 20 candidates | <60s | Batch Claude calls |
| Database query | <100ms | Indexed queries |
| API response | <1s | Async handlers |

---

## 9. Security Measures

### 9.1 Input Validation

```python
from pydantic import BaseModel, Field, validator

class UploadRequest(BaseModel):
    job_id: UUID
    max_resumes: int = Field(default=50, le=50)
    
    @validator('job_id')
    def validate_job_id(cls, v):
        # Validate UUID format
        if not isinstance(v, UUID):
            raise ValueError('Invalid job ID format')
        return v

class FileValidation:
    ALLOWED_MIMES = {
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
    }
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def validate_file(file):
        if file.content_type not in FileValidation.ALLOWED_MIMES:
            raise ValueError("Invalid file type")
        if file.size > FileValidation.MAX_SIZE:
            raise ValueError("File too large")
        return True
```

### 9.2 Database Security

- Use parameterized queries (SQLAlchemy handles this)
- Encrypt sensitive columns
- Use connection pooling
- Implement row-level security (future)

### 9.3 API Security

```python
from fastapi import HTTPException, status

def verify_request_signature(request, signature):
    """Verify request authenticity (future feature)"""
    pass

@app.middleware("http")
async def validate_content_type(request, call_next):
    if request.method in ["POST", "PUT"]:
        if "application/json" not in request.headers.get("content-type", ""):
            raise HTTPException(status_code=400, detail="Invalid content type")
    return await call_next(request)
```

---

## 10. Deployment Configuration

### 10.1 Docker Setup

**Dockerfile (Backend):**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: recruiter
      POSTGRES_USER: recruiter
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://recruiter:${DB_PASSWORD}@db:5432/recruiter
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    depends_on:
      - db

volumes:
  postgres_data:
```

### 10.2 Environment Variables

**.env (Backend):**
```
ANTHROPIC_API_KEY=sk-...
DATABASE_URL=postgresql://user:pass@localhost/recruiter
ENVIRONMENT=development
LOG_LEVEL=INFO
MAX_FILE_SIZE=10485760
UPLOAD_DIR=/tmp/uploads
```

---

## 11. Monitoring & Logging

### 11.1 Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/recruitment-engine.log'),
        RotatingFileHandler(
            '/var/log/recruitment-engine.log',
            maxBytes=10485760,  # 10MB
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usage
logger.info(f"Processing resume: {filename}")
logger.error(f"Claude API error: {error_message}")
```

### 11.2 Metrics to Track

- API response times
- Error rates by endpoint
- Claude API usage (tokens, cost)
- Database query performance
- File processing duration
- Match score distribution

---

## 12. Testing Strategy

### 12.1 Unit Tests

```python
# tests/test_skill_extractor.py
import pytest
from services.skill_extractor import extract_skills_from_resume

def test_extract_skills_from_resume():
    resume_text = "Python developer with 5 years experience..."
    skills = extract_skills_from_resume(resume_text)
    
    assert "Python" in skills['technical_skills']
    assert skills['years_experience'] == 5

def test_invalid_resume():
    with pytest.raises(ValueError):
        extract_skills_from_resume("")
```

### 12.2 Integration Tests

```python
# tests/test_analyze_endpoint.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_endpoint():
    response = client.post("/api/analyze/job-123", json={})
    assert response.status_code == 200
    assert "candidates_ranked" in response.json()["data"]
```

---

## 13. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-22 | Initial technical specifications |
