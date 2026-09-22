# AI Recruitment Intelligence Engine (RIE)

An AI-powered resume screening, skill extraction, and candidate ranking system built with **FastAPI (Python)**, **Next.js 14 (TypeScript)**, **Tailwind CSS**, and **Claude Opus AI**.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│  Next.js 14 (App Router, TypeScript, Tailwind CSS)          │
│  Port: 3000                                                 │
│  ├── / (Home / Landing / Job Overview)                       │
│  ├── /jobs/new (Job Description & AI Requirements Input)    │
│  ├── /jobs/[jobId]/upload (Drag & Drop Resume Upload)       │
│  ├── /results/[jobId] (Ranked Results Dashboard & Badges)   │
│  └── /compare (Side-by-Side Candidate Comparison Matrix)    │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP / REST API (JSON)
┌───────────────────────────▼─────────────────────────────────┐
│                    Backend Layer                             │
│  FastAPI (Python 3.10+)                                     │
│  Port: 8000                                                 │
│  ├── File Processor (PyPDF2, python-docx, TXT normalization)│
│  ├── AI Skill Extractor (Claude Opus 4.1 + NLP Heuristics)  │
│  ├── Matcher & Scorer (0.5 Tech + 0.3 Exp + 0.2 Soft)       │
│  ├── Ranker & Assessor (Multi-tier sort & assessment)       │
│  └── SQLAlchemy 2.0 ORM (PostgreSQL / SQLite dialect support)│
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    PostgreSQL        Anthropic Claude     File Storage
 (or SQLite Local)   (Opus 4.1 20250805)   (Auto-cleaned)
```

---

## Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm 9+

### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run FastAPI backend server (port 8000)
uvicorn main:app --reload --port 8000
```

The backend will automatically create SQLite database tables on startup (or connect to PostgreSQL if `DATABASE_URL` is set in `backend/.env`).
- Interactive Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

### 3. Frontend Setup
```bash
# In a separate terminal, navigate to frontend
cd frontend

# Install dependencies (if not already installed)
npm install

# Run Next.js development server (port 3000)
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Running Automated Tests

Run the comprehensive unit and integration test suite with coverage report:

```bash
cd backend
PYTHONPATH=. ./venv/bin/pytest --cov=. --cov-report=term-missing tests/ -v
```

**Coverage**: 83%+ test coverage across all business logic, matching algorithms, file parsing, and API routes.

---

## User Flow & Features

1. **Step 1: Create Job Posting** (`/jobs/new`)
   - Input job title and paste full job description.
   - Claude AI extracts required technical skills, soft skills, nice-to-have skills, minimum experience years, and seniority level.

2. **Step 2: Upload Resumes** (`/jobs/[jobId]/upload`)
   - Drag-and-drop or browse multiple resumes (PDF, DOCX, TXT) up to 10MB each.
   - Automatic text parsing and asynchronous storage.

3. **Step 3: AI Analysis & Ranking** (`/results/[jobId]`)
   - Quantified match score calculated:
     $$\text{Overall} = (0.5 \times \text{Tech}) + (0.3 \times \text{Experience}) + (0.2 \times \text{Soft}) - \text{Penalties}$$
   - Visual badges:
     - <span style="color:#00B359">Green</span>: Matched skills
     - <span style="color:#D94A45">Red</span>: Missing critical skills
     - <span style="color:#666666">Gray</span>: Extra/bonus skills
   - Recruiter evaluation assessment for each candidate.
   - Detailed modal with complete profile breakdown.
   - Export results to CSV.

4. **Step 4: Side-by-Side Comparison** (`/compare`)
   - Select 2-5 candidates to compare key metrics and view a detailed skill matrix.
   - AI executive recommendation comparing strengths and gaps.
   - Print/Save as PDF.

---

## Test Data

5 pre-generated test resumes are included in `test_data/resumes/`:
- `alex_senior_python.pdf` (Senior Python Engineer, 7 yrs, FastAPI, PostgreSQL, Docker, AWS)
- `sarah_mid_python.docx` (Mid-level Python Developer, 4 yrs, Django, PostgreSQL, Git)
- `jordan_junior_python.txt` (Junior Developer, 1 yr, Flask, SQLite)
- `emily_frontend_lead.pdf` (Frontend Lead, React, TypeScript)
- `michael_devops_cloud.txt` (DevOps & Cloud Engineer, AWS, Kubernetes, Docker, Python)

To regenerate sample resumes at any time:
```bash
./backend/venv/bin/python test_data/generate_resumes.py
```

---

## Docker Deployment

To launch PostgreSQL, backend, and frontend via Docker Compose:
```bash
docker-compose up --build
```
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)
