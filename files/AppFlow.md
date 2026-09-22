# AppFlow.md
## Application Flow & Architecture - Recruitment Intelligence Engine

---

## 1. High-Level System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                      USER'S BROWSER                            │
│                                                                │
│  Next.js Frontend (TypeScript + React)                        │
│  ├── Pages: Home, Upload, Results, Compare                   │
│  ├── Components: CandidateCard, ProgressBar, etc.            │
│  ├── API Client: axios calls to backend                      │
│  └── State Management: React Context                         │
└───────────────────┬────────────────────────────────────────────┘
                    │
              HTTP REST API
          (JSON requests/responses)
                    │
┌───────────────────▼────────────────────────────────────────────┐
│              BACKEND SERVER (Python FastAPI)                  │
│                                                                │
│  API Layer (Routes)                                           │
│  ├── POST /api/jobs              (Create job)                │
│  ├── POST /api/upload             (Upload resumes)           │
│  ├── POST /api/analyze/{job_id}   (Run analysis)            │
│  ├── GET  /api/results/{job_id}   (Fetch results)          │
│  └── GET  /api/export/{job_id}    (Export CSV)             │
│                                                                │
│  Service Layer (Business Logic)                              │
│  ├── file_processor.py            (Extract text)            │
│  ├── skill_extractor.py           (Claude API calls)        │
│  ├── matcher.py                   (Compare skills)          │
│  └── ranker.py                    (Sort candidates)         │
│                                                                │
│  Database Layer (SQLAlchemy ORM)                            │
│  ├── models/database.py           (DB schemas)              │
│  └── Async database connections                             │
└───────────────────┬────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┬────────────┐
        │           │           │            │
    PostgreSQL  Claude API  File System   (Future: S3)
    (Data)      (AI Skills) (Temp files)
```

---

## 2. Request-Response Flow: Complete Lifecycle

### 2.1 User Creates Job

```
┌─ FRONTEND ─────────────────────────────────────────┐
│                                                    │
│ User enters:                                       │
│  - Job Title: "Python Developer"                  │
│  - Description: "We need a Python expert..."      │
│                                                    │
│ Clicks "Create Job"                               │
│                                                    │
│ Frontend Action:                                   │
│  POST /api/jobs                                   │
│  Body: {                                           │
│    "title": "Python Developer",                   │
│    "description": "..."                           │
│  }                                                 │
│                                                    │
└───────────────────┬────────────────────────────────┘
                    │
            REQUEST TRAVELS
                    │
┌───────────────────▼────────────────────────────────┐
│ BACKEND - Route Handler (main.py)                 │
│                                                    │
│ @app.post("/api/jobs")                            │
│ async def create_job(request: JobSchema):         │
│                                                    │
│  1. Validate input (Pydantic)                     │
│  2. Save job to database:                         │
│     INSERT INTO job_postings (title, desc, ...)  │
│  3. Extract requirements via Claude:              │
│     - Send description to Claude                  │
│     - Claude returns JSON:                        │
│       {                                            │
│         "required_skills": [...],                 │
│         "years_experience": 5,                    │
│         ...                                        │
│       }                                            │
│  4. Update job_postings.extracted_requirements    │
│  5. Return response:                              │
│     {                                              │
│       "success": true,                            │
│       "job_id": "uuid-here",                      │
│       "extracted_requirements": {...}             │
│     }                                              │
│                                                    │
└───────────────────┬────────────────────────────────┘
                    │
            RESPONSE RETURNS
                    │
┌───────────────────▼────────────────────────────────┐
│ FRONTEND                                           │
│                                                    │
│ Receives response:                                │
│  {                                                 │
│    "success": true,                               │
│    "job_id": "abc123"                             │
│  }                                                 │
│                                                    │
│ Actions:                                           │
│  1. Store job_id in URL/session                   │
│  2. Redirect to upload page                       │
│  3. Show: "Job created! Upload resumes now"       │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 2.2 User Uploads Resumes

```
┌─ FRONTEND ─────────────────────────────────────────┐
│                                                    │
│ User drags 20 PDF files into upload zone          │
│                                                    │
│ Frontend Action:                                   │
│  POST /api/upload (multipart/form-data)           │
│  Files: [john.pdf, jane.pdf, ..., alex.pdf]       │
│  Data: {"job_id": "abc123"}                       │
│                                                    │
│ Shows progress:                                    │
│  "Uploading: 45% (9 of 20 files)"                 │
│                                                    │
└───────────────────┬────────────────────────────────┘
                    │
        MULTIPART UPLOAD
                    │
┌───────────────────▼────────────────────────────────┐
│ BACKEND - Upload Handler                          │
│                                                    │
│ @app.post("/api/upload")                          │
│ async def upload_resumes(files: List[UploadFile]):│
│                                                    │
│  For each file:                                    │
│    1. Validate:                                    │
│       - Check MIME type                           │
│       - Check size < 10MB                         │
│       - Scan for malware (future)                │
│                                                    │
│    2. Save temporarily:                           │
│       - Write to /tmp/uploads/                    │
│                                                    │
│    3. Extract text:                               │
│       if .pdf:  use PyPDF2 (+ OCR if needed)      │
│       if .docx: use python-docx                   │
│       if .txt:  read directly                     │
│                                                    │
│    4. Store in database:                          │
│       INSERT INTO candidates (                    │
│         job_id,                                    │
│         filename,                                  │
│         original_text,                            │
│         extracted_skills: {} (empty for now)      │
│       )                                            │
│                                                    │
│    5. Delete temporary file                       │
│                                                    │
│  Return response:                                  │
│  {                                                 │
│    "success": true,                               │
│    "uploaded": 20,                                │
│    "failed": 0,                                   │
│    "candidates": [...]                            │
│  }                                                 │
│                                                    │
└───────────────────┬────────────────────────────────┘
                    │
            RESPONSE RETURNS
                    │
┌───────────────────▼────────────────────────────────┐
│ FRONTEND                                           │
│                                                    │
│ Shows:                                             │
│  ✓ 20 files uploaded                              │
│  ✓ john.pdf                                       │
│  ✓ jane.pdf                                       │
│  ... (all with green checkmarks)                  │
│                                                    │
│ Button: [Analyze] becomes active                  │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 2.3 User Analyzes (Main Flow)

```
┌─ FRONTEND ─────────────────────────────────────────┐
│                                                    │
│ User clicks [Analyze] button                      │
│                                                    │
│ Frontend Action:                                   │
│  POST /api/analyze/{job_id}                       │
│  Body: {"job_id": "abc123"}                       │
│                                                    │
│ Shows: "Analyzing candidates..." + progress bar   │
│                                                    │
└───────────────────┬────────────────────────────────┘
                    │
            REQUEST SENT
                    │
┌───────────────────▼────────────────────────────────┐
│ BACKEND - Analysis Handler                        │
│                                                    │
│ @app.post("/api/analyze/{job_id}")                │
│ async def analyze(job_id: UUID):                  │
│                                                    │
│  PHASE 1: Load Data                               │
│  ├─ SELECT * FROM candidates WHERE job_id = ?    │
│  ├─ SELECT * FROM job_postings WHERE id = ?      │
│  └─ Confirm: 20 candidates + 1 job loaded        │
│                                                    │
│  PHASE 2: Extract Skills from Resumes (if not done)
│  ├─ For each candidate:                           │
│  │   ├─ Call Claude API:                          │
│  │   │    "Extract skills from this resume: ..." │
│  │   ├─ Claude returns JSON                       │
│  │   ├─ Parse & validate JSON                     │
│  │   ├─ UPDATE candidates.extracted_skills = {}  │
│  │   └─ Log: "Extracted skills for john.pdf"     │
│  │                                                │
│  │  Time: ~30s per resume × 20 = 10 minutes      │
│  │  (Can optimize with batch Claude calls)       │
│  └─ Done: All candidates now have skills         │
│                                                    │
│  PHASE 3: Extract Requirements from Job (if not done)
│  ├─ Claude already did this when job was created │
│  ├─ Retrieve: job_postings.extracted_requirements│
│  └─ Example: {required_tech: [...], years: 5}   │
│                                                    │
│  PHASE 4: Match & Calculate Scores               │
│  ├─ For each candidate:                           │
│  │   ├─ Compare candidate.skills vs job.requirements
│  │   ├─ Use matching algorithm:                   │
│  │   │    Tech Match = matched_skills / required │
│  │   │    Exp Match = min(years_exp / req, 1.0)  │
│  │   │    Soft Match = soft_skills_found / req   │
│  │   │    Overall = (Tech×0.5) + (Exp×0.3) + ... │
│  │   │    Penalties for critical missing skills  │
│  │   ├─ Identify:                                 │
│  │   │    - matched_skills                       │
│  │   │    - missing_skills                       │
│  │   │    - extra_skills                         │
│  │   └─ Generate brief assessment text           │
│  │                                                │
│  │  Time: ~1s per candidate × 20 = 20s          │
│  └─ Done: All scores calculated                  │
│                                                    │
│  PHASE 5: Rank Candidates                        │
│  ├─ Sort by match_score DESC                     │
│  ├─ Assign rank: 1, 2, 3, ..., 20                │
│  └─ Tie-break by years_experience if scores same │
│                                                    │
│  PHASE 6: Store Results                          │
│  ├─ INSERT INTO job_matches:                      │
│  │    For each candidate:                         │
│  │    - candidate_id                              │
│  │    - job_id                                    │
│  │    - match_score                               │
│  │    - matched_skills JSON                      │
│  │    - missing_skills JSON                      │
│  │    - assessment text                          │
│  │    - rank                                      │
│  └─ Done: 20 rows inserted                       │
│                                                    │
│  RETURN RESPONSE:                                 │
│  {                                                 │
│    "success": true,                               │
│    "analysis_complete": true,                     │
│    "candidates_ranked": 20,                       │
│    "top_match": {                                 │
│      "name": "John Doe",                          │
│      "match_score": 92                            │
│    }                                              │
│  }                                                 │
│                                                    │
│  Total time: ~30-60 seconds (or ~10 min if first │
│  time extracting skills from resumes)            │
│                                                    │
└───────────────────┬────────────────────────────────┘
                    │
            RESPONSE RETURNS
                    │
┌───────────────────▼────────────────────────────────┐
│ FRONTEND                                           │
│                                                    │
│ Receives: {"success": true, "analysis_complete"}  │
│                                                    │
│ Action:                                            │
│  1. Redirect to results page                      │
│  2. Fetch results data                            │
│  3. Display ranked list                           │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 2.4 User Views Results

```
┌─ FRONTEND ─────────────────────────────────────────┐
│                                                    │
│ Results page loads automatically                  │
│                                                    │
│ Frontend Action:                                   │
│  GET /api/results/{job_id}                        │
│                                                    │
│ Shows: Ranked list of 20 candidates               │
│                                                    │
└───────────────────┬────────────────────────────────┘
                    │
            REQUEST SENT
                    │
┌───────────────────▼────────────────────────────────┐
│ BACKEND - Results Handler                         │
│                                                    │
│ @app.get("/api/results/{job_id}")                 │
│ async def get_results(job_id: UUID):              │
│                                                    │
│  Query:                                            │
│  SELECT * FROM job_matches                        │
│  WHERE job_id = ?                                 │
│  ORDER BY rank ASC                                │
│                                                    │
│  Return:                                           │
│  {                                                 │
│    "candidates": [                                │
│      {                                             │
│        "rank": 1,                                  │
│        "name": "John Doe",                         │
│        "match_score": 92,                          │
│        "matched_skills": ["Python", "FastAPI"],  │
│        "missing_skills": ["AWS"],                │
│        "extra_skills": ["Java", "React"]         │
│      },                                            │
│      { rank: 2, ... },                            │
│      ...                                           │
│    ]                                               │
│  }                                                 │
│                                                    │
└───────────────────┬────────────────────────────────┘
                    │
            RESPONSE RETURNS
                    │
┌───────────────────▼────────────────────────────────┐
│ FRONTEND                                           │
│                                                    │
│ Displays:                                          │
│  [Card 1] John Doe  ████████████░ 92%             │
│  [Card 2] Jane Smith ████████░░░ 85%              │
│  [Card 3-20] ...                                  │
│                                                    │
│ User can:                                          │
│  - Click for details                              │
│  - Compare candidates                             │
│  - Export as CSV                                  │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 3. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ INPUT LAYER                                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Resume Files              Job Description             │
│  (PDF, DOCX, TXT)          (Text paste)               │
│         │                         │                    │
│         └──────────┬──────────────┘                    │
│                    │                                   │
├─────────────────────▼──────────────────────────────────┤
│ PROCESSING LAYER                                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Text Extraction              Requirement Extraction   │
│  (PyPDF2/OCR/etc)             (Claude API)            │
│         │                         │                    │
│         └──────────┬──────────────┘                    │
│                    │                                   │
│         Normalized Text Data                           │
│                    │                                   │
├─────────────────────▼──────────────────────────────────┤
│ AI EXTRACTION LAYER                                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Claude API: Extract Skills from Resumes              │
│  Claude API: Extract Requirements from Job            │
│         │                                              │
│         ├─ Resume Skills: Technical, Soft, Certs      │
│         └─ Job Requirements: Required, Nice-to-have   │
│                                                         │
│         Extracted JSON Data                            │
│                    │                                   │
├─────────────────────▼──────────────────────────────────┤
│ DATABASE LAYER                                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  candidates table                job_postings table    │
│  ├─ id                           ├─ id                │
│  ├─ original_text                ├─ extracted_reqs    │
│  ├─ extracted_skills             └─ ...               │
│  └─ ...                                                │
│                    │                                   │
├─────────────────────▼──────────────────────────────────┤
│ MATCHING & RANKING LAYER                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  For Each Candidate:                                   │
│  ├─ Compare skills (matcher.py)                       │
│  ├─ Calculate score (ranker.py)                       │
│  ├─ Identify gaps                                      │
│  └─ Generate assessment                               │
│                                                         │
│  job_matches table                                     │
│  ├─ candidate_id                                       │
│  ├─ job_id                                            │
│  ├─ match_score                                        │
│  ├─ matched_skills                                     │
│  ├─ missing_skills                                     │
│  ├─ rank                                               │
│  └─ assessment                                         │
│                    │                                   │
├─────────────────────▼──────────────────────────────────┤
│ OUTPUT LAYER                                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Results Display               Export Formats          │
│  ├─ Ranked candidate list      ├─ CSV download        │
│  ├─ Match percentages          ├─ PDF comparison      │
│  ├─ Skill badges               └─ JSON API            │
│  ├─ Comparison view                                    │
│  └─ Detail modals                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Key Application States

```
┌─────────────────────────────────────────────────┐
│ STATE MACHINE - Application Flow                │
├─────────────────────────────────────────────────┤
│                                                 │
│ IDLE                                            │
│ └─ User on home page, no active job            │
│    Transitions:                                 │
│    → CREATE_JOB (user clicks create job)       │
│                                                 │
│ CREATE_JOB                                      │
│ └─ User filling job form                       │
│    Transitions:                                 │
│    → UPLOAD_RESUMES (form submitted, job saved)│
│    → IDLE (user clicks cancel)                 │
│                                                 │
│ UPLOAD_RESUMES                                  │
│ └─ User uploading resume files                 │
│    Transitions:                                 │
│    → ANALYZING (user clicks analyze)           │
│    → UPLOAD_RESUMES (retry on error)           │
│    → CREATE_JOB (user clicks back)             │
│                                                 │
│ ANALYZING                                       │
│ └─ Backend processing (Claude API calls)       │
│    Transitions:                                 │
│    → VIEWING_RESULTS (analysis complete)       │
│    → ANALYZING (retry on error)                │
│                                                 │
│ VIEWING_RESULTS                                 │
│ └─ User viewing ranked candidate list          │
│    Transitions:                                 │
│    → CANDIDATE_DETAILS (user clicks details)   │
│    → COMPARING (user selects for comparison)   │
│    → EXPORTING (user clicks export)            │
│    → IDLE (user starts new analysis)           │
│                                                 │
│ CANDIDATE_DETAILS                               │
│ └─ Modal showing full candidate info           │
│    Transitions:                                 │
│    → VIEWING_RESULTS (user closes modal)       │
│                                                 │
│ COMPARING                                       │
│ └─ Side-by-side candidate comparison           │
│    Transitions:                                 │
│    → VIEWING_RESULTS (user clicks back)        │
│    → EXPORTING (user exports comparison)       │
│                                                 │
│ EXPORTING                                       │
│ └─ Generating & downloading export file        │
│    Transitions:                                 │
│    → VIEWING_RESULTS (download complete)       │
│    → COMPARING (if comparing + export)         │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 5. Error Handling Flow

```
┌─ USER ACTION ─────────────────────────┐
│                                       │
│  User uploads file                   │
│                                       │
└─────────────┬───────────────────────────┘
              │
    ┌─────────▼──────────┐
    │ Input Validation   │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────────────────┐
    │ Is file valid?                 │
    └─────────┬──────────┬───────────┘
              │          │
           YES          NO
              │          │
    ┌─────────▼──┐   ┌────▼─────────────────┐
    │ Process    │   │ Error Handler        │
    │ file       │   │                      │
    └─────────┬──┘   │ 1. Catch exception   │
              │      │ 2. Log error         │
              │      │ 3. Return JSON error │
              │      │ 4. Show user message │
              │      └────┬─────────────────┘
              │           │
              └───────┬───┘
                      │
            ┌─────────▼──────────┐
            │ Send to frontend   │
            │ {                  │
            │  "error": true,    │
            │  "message": "..."  │
            │ }                  │
            └────────┬───────────┘
                     │
            ┌────────▼────────────┐
            │ Frontend displays   │
            │ error message to    │
            │ user                │
            │ [Retry] [Cancel]    │
            └─────────────────────┘
```

---

## 6. Caching Strategy

```
Claude API Responses: Cache extracted skills
├─ If same resume uploaded again
├─ Use cached skills (skip Claude call)
├─ Save API costs & time
└─ Use file hash to identify duplicates

Database Queries: Use connection pooling
├─ Reuse connections (don't create new each time)
├─ Reduces latency
└─ Handles concurrent requests

Job Requirements: Cache after extraction
├─ Same job can have multiple uploads
├─ Extract once, reuse for all candidate uploads
└─ Saves Claude API calls

Browser: No caching for results
├─ Always fetch latest from backend
├─ Don't cache ranked list locally
└─ Ensures accuracy
```

---

## 7. Concurrent Request Handling

```
Scenario: User uploads 20 resumes, all being processed

Frontend:
├─ Submits 20 file uploads
├─ Shows progress: "5 of 20 uploaded"
└─ Once all uploaded, triggers /api/analyze

Backend:
├─ Receives 20 upload requests (async)
├─ Processes in parallel (up to 5 at a time)
├─ Stores each in database
└─ Returns upload confirmation

Claude API:
├─ Skill extraction can also be parallelized
├─ Send 3-5 resumes in batch prompts
├─ Reduces roundtrips to Claude
└─ Stays within rate limits

Database:
├─ Connection pool (10-20 connections)
├─ Each request uses one connection
├─ Transactions ensure data consistency
└─ No race conditions (constraints + locks)
```

---

## 8. Failure Recovery

### 8.1 Claude API Fails

```
Scenario: Claude API returns 500 error during skill extraction

Flow:
├─ Backend catches error
├─ Logs: "Claude API error for resume: john.pdf"
├─ Retries with exponential backoff:
│  ├─ Wait 1 second, retry
│  ├─ Wait 2 seconds, retry
│  ├─ Wait 4 seconds, retry
│  └─ After 3 failures, return error to user
├─ Frontend shows: "Service temporarily unavailable. Try again?"
└─ User can retry

Prevention:
├─ Rate limit monitoring
├─ Health checks to Claude API
├─ Fallback to simpler skill extraction (regex) if needed
└─ Alert admin if repeated failures
```

### 8.2 Database Connection Lost

```
Scenario: PostgreSQL becomes unavailable mid-analysis

Flow:
├─ Backend detects connection error
├─ Connection pool tries to reconnect
├─ After 3 reconnection attempts, return error
├─ Frontend shows: "Database error. Please try again."
└─ Data loss: None (transaction rolled back)

Prevention:
├─ Database auto-restarts in production
├─ Connection pooling with health checks
├─ Monitoring alerts if DB is down
└─ Regular backups (automatic)
```

### 8.3 File Upload Interrupted

```
Scenario: Network drops during file upload (60% complete)

Flow:
├─ Frontend detects connection loss
├─ Shows: "Upload interrupted"
├─ Partial files in database are cleaned up (optional)
├─ User can retry or start over
└─ No incomplete data remains

Prevention:
├─ Implement resumable uploads (future)
├─ Store upload checkpoints
├─ Allow resume from last successful chunk
└─ Track upload state in browser (localStorage)
```

---

## 9. Performance Optimization Strategies

### 9.1 Backend Optimizations

```
1. Batch Claude Requests
   ├─ Instead of: 20 sequential calls (400s)
   ├─ Do: 4 batch calls with 5 resumes each (~100s)
   └─ Saves: 75% time

2. Database Indexing
   ├─ CREATE INDEX on job_id (candidates table)
   ├─ CREATE INDEX on job_id (job_matches table)
   ├─ CREATE INDEX on match_score (for sorting)
   └─ Query time: <100ms vs 5s

3. Async Processing
   ├─ Don't wait for Claude
   ├─ Submit skill extraction as background task
   ├─ Return immediately to user: "Processing..."
   └─ User notified when ready

4. Connection Pooling
   ├─ Reuse PostgreSQL connections
   ├─ Pool size: 10-20 connections
   └─ Reduces connection overhead
```

### 9.2 Frontend Optimizations

```
1. Lazy Loading
   ├─ Only load candidate details when expanded
   ├─ Don't load all 20 candidates' details upfront
   └─ Improves initial load time

2. Pagination
   ├─ Show 10 candidates per page
   ├─ User can click "Next" for 11-20
   └─ Reduces DOM nodes

3. Component Memoization
   ├─ Prevent re-renders of CandidateCard
   ├─ Use React.memo() for cards
   └─ Smoother scrolling

4. Code Splitting
   ├─ Load Results page code only when needed
   ├─ Not on home page load
   └─ Faster initial load
```

---

## 10. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-22 | Initial application flow documentation |
