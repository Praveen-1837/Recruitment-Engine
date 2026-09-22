# Tracer.md
## User Flows & Interaction Tracing - Recruitment Intelligence Engine

---

## 1. Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   USER JOURNEY MAP                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. HOME PAGE          2. INPUT PHASE       3. ANALYSIS         │
│  ├─ Visit app          ├─ Upload resumes    ├─ Processing      │
│  ├─ See instructions   ├─ Input job desc    ├─ Extracting skills
│  └─ Start workflow     └─ Click Analyze     └─ Ranking         │
│                                                                 │
│  4. RESULTS            5. REVIEW            6. ACTION           │
│  ├─ View ranked list   ├─ Click candidate   ├─ Compare          │
│  ├─ See match scores   ├─ View details      ├─ Export           │
│  └─ See skill gaps     └─ Expand skills     └─ Take notes       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Primary User Flow: Full Recruitment Cycle

### 2.1 Happy Path - Complete Flow

```
┌──────────────┐
│ 1. VISIT APP │
└──────┬───────┘
       │
       ├─► User navigates to app.recruitment-engine.com
       ├─► Lands on Home Page
       ├─► Sees title: "AI Recruitment Intelligence Engine"
       ├─► Sees CTA: "Get Started" button
       └─► Sees instructions and features overview

┌──────────────────────┐
│ 2. CREATE NEW JOB    │
└──────┬───────────────┘
       │
       ├─► Clicks "Create New Job" or "New Analysis"
       ├─► Form appears:
       │   ├─ Job Title input
       │   ├─ Job Description textarea (large)
       │   └─ Create button
       ├─► Enters "Python Developer"
       ├─► Pastes full job description
       ├─► Clicks "Create Job"
       └─► Backend: Sends job to Claude for requirement extraction

┌──────────────────────┐
│ 3. UPLOAD RESUMES    │
└──────┬───────────────┘
       │
       ├─► Redirected to Upload page
       ├─► Sees: "Upload Resumes"
       ├─► Sees upload area with instructions
       ├─► Option 1: Drags 20 PDF files into drop zone
       ├─► Option 2: Clicks "Browse" and selects files
       ├─► Progress bar shows file uploads (90% complete)
       ├─► Files appear in list below:
       │   ├─ john_doe.pdf ✓
       │   ├─ jane_smith.pdf ✓
       │   ├─ alex_johnson.pdf ✓
       │   └─ (17 more files)
       ├─► All files green checkmark (uploaded)
       └─► Clicks "Analyze" button (bottom)

┌──────────────────────┐
│ 4. PROCESSING        │
└──────┬───────────────┘
       │
       ├─► Page shows "Analyzing candidates..."
       ├─► Progress indicator with steps:
       │   ├─ ✓ Extracting text from resumes (100%)
       │   ├─ ⟳ Extracting skills from resumes (45%)
       │   └─ ⠿ Comparing with job requirements...
       ├─► Estimated time: 2 minutes remaining
       └─► User waits or can close/leave (background processing)

┌──────────────────────┐
│ 5. VIEW RESULTS      │
└──────┬───────────────┘
       │
       ├─► Results page loads automatically
       ├─► Top of page shows:
       │   ├─ Job title: "Python Developer"
       │   ├─ Total candidates analyzed: 20
       │   └─ Analysis completed: 2 min 34 sec
       ├─► Candidate list appears with ranking:
       │   │
       │   ├─► Card 1: "John Doe" (john_doe.pdf)
       │   │   ├─ Rank: #1
       │   │   ├─ Match Score: 92%
       │   │   ├─ Visual bar: ████████████░ (92%)
       │   │   ├─ Matched Skills (green badges):
       │   │   │  ✓ Python ✓ FastAPI ✓ PostgreSQL
       │   │   ├─ Missing Skills (red badges):
       │   │   │  ✗ AWS ✗ Docker
       │   │   └─ [View Details ▼]
       │   │
       │   ├─► Card 2: "Jane Smith" (jane_smith.pdf)
       │   │   ├─ Rank: #2
       │   │   ├─ Match Score: 85%
       │   │   ├─ Visual bar: ████████░░
       │   │   ├─ Matched Skills: ✓ Python ✓ PostgreSQL
       │   │   ├─ Missing Skills: ✗ FastAPI ✗ AWS ✗ Docker
       │   │   └─ [View Details ▼]
       │   │
       │   └─► Card 3-20: (similar format, lower scores)
       │
       └─► Bottom of page: [Export CSV] [Export PDF]

┌──────────────────────┐
│ 6. REVIEW CANDIDATE  │
└──────┬───────────────┘
       │
       ├─► User clicks "View Details" on John Doe's card
       ├─► Candidate detail modal/page opens
       ├─► Shows:
       │   ├─ Candidate name: John Doe
       │   ├─ Filename: john_doe.pdf
       │   ├─ Match Score: 92%
       │   ├─ All Matched Skills:
       │   │  ✓ Python (Technical)
       │   │  ✓ FastAPI (Framework)
       │   │  ✓ PostgreSQL (Database)
       │   │  ✓ Docker (Tool)
       │   │  ✓ Leadership (Soft Skill)
       │   ├─ Missing Skills:
       │   │  ✗ AWS (Cloud - CRITICAL)
       │   │  ✗ Kubernetes
       │   ├─ Extra Skills Candidate Has:
       │   │  + Java
       │   │  + React
       │   ├─ Experience: 5 years (Meets requirement)
       │   ├─ Certifications: AWS Solutions Architect (ironically)
       │   └─ Assessment:
       │      "Strong match. Candidate has all core Python 
       │       and database skills. Missing AWS but has 
       │       equivalent cloud platform experience."
       │
       └─► User closes modal (back to results)

┌──────────────────────┐
│ 7. COMPARE           │
└──────┬───────────────┘
       │
       ├─► User wants to compare top candidates
       ├─► Clicks checkbox next to "John Doe" (Card 1)
       ├─► Clicks checkbox next to "Jane Smith" (Card 2)
       ├─► [Compare Selected] button becomes active
       ├─► Clicks "Compare Selected"
       │
       └─► Comparison page loads:
           │
           ├─ Page title: "Candidate Comparison"
           ├─ Table format:
           │
           │  ┌────────────────┬──────────┬──────────┐
           │  │ Criteria       │ John Doe │ Jane Smith
           │  ├────────────────┼──────────┼──────────┤
           │  │ Match Score    │ 92%      │ 85%
           │  │ Years Exp      │ 5 years  │ 3 years
           │  │ Tech Skills    │ 7/8      │ 5/8
           │  │ Missing Skills │ 2        │ 4
           │  │ Soft Skills    │ Strong   │ Good
           │  └────────────────┴──────────┴──────────┘
           │
           ├─ Detailed skill comparison:
           │  ┌─────────────────────────────────────┐
           │  │         Matched Skills               │
           │  ├────────────────┬──────────┬──────────┤
           │  │ Skill          │ John     │ Jane     │
           │  ├────────────────┼──────────┼──────────┤
           │  │ Python         │ ✓        │ ✓        │
           │  │ FastAPI        │ ✓        │ ✗        │
           │  │ PostgreSQL     │ ✓        │ ✓        │
           │  │ AWS            │ ✗        │ ✗        │
           │  │ Docker         │ ✓        │ ✗        │
           │  └────────────────┴──────────┴──────────┘
           │
           ├─ Recommendation section:
           │  "John Doe is the stronger match overall.
           │   Both have Python skills, but John has
           │   more complete tech stack match."
           │
           └─ [Export Comparison] [Back to Results]

┌──────────────────────┐
│ 8. EXPORT RESULTS    │
└──────┬───────────────┘
       │
       ├─► User clicks "Export CSV" button
       ├─► File downloaded: recruitment_analysis_2026-09-22.csv
       ├─► Format:
       │   rank,filename,name,match_score,matched_skills,missing_skills,experience
       │   1,john_doe.pdf,John Doe,92,"Python, FastAPI, PostgreSQL","AWS, Kubernetes",5
       │   2,jane_smith.pdf,Jane Smith,85,"Python, PostgreSQL","FastAPI, AWS, Docker",3
       │   ...
       │
       └─► User imports into Excel or shares with hiring manager
```

---

## 3. Alternative Flows

### 3.1 Error: Invalid Job Description
```
┌─ User enters empty/too short job description
├─ Clicks "Create Job"
├─ Error appears: "Job description must be at least 200 characters"
├─ Input field highlighted in red
├─ User fixes and resubmits
└─ Process continues
```

### 3.2 Error: No Resumes Uploaded
```
┌─ User is on upload page with 0 files
├─ Clicks "Analyze" button
├─ Error appears: "Please upload at least 1 resume"
├─ Upload zone highlighted
├─ User adds files
└─ Process continues
```

### 3.3 Error: File Upload Failed
```
┌─ User uploads 20 files
├─ File #5 fails (corrupted PDF)
├─ Alert appears: "jane_smith.pdf failed to upload (Invalid file)"
├─ File shown with red X in list
├─ Option to retry or continue without this file
├─ User clicks "Continue with 19 files"
└─ Process continues with remaining files
```

### 3.4 Batch Upload Cancelled
```
┌─ User is uploading 20 files (50% complete)
├─ Clicks "Cancel Upload" button
├─ Confirmation modal: "Cancel upload? Progress will be lost"
├─ User confirms
├─ Returns to home page
├─ Job is deleted (not analyzed)
└─ User can start over
```

### 3.5 Refining Results
```
┌─ User sees results
├─ Disagrees with rank of candidate #3
├─ Clicks "Provide Feedback" (future)
├─ Feedback form opens
├─ Selects: "This candidate ranked too low"
├─ Optional comment: "They have AWS experience, not listed in resume"
├─ Submits feedback
└─ System learns for next analysis
```

---

## 4. State Transitions

### 4.1 Application States

```
┌─────────────────────────────────────────────────────────────┐
│ State Diagram - Recruitment Analysis                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ (Start) ─→ IDLE ─→ INPUT_JOB                               │
│              ↑         │                                   │
│              │         └─→ INPUT_RESUMES                   │
│              │              │                              │
│              │              └─→ PROCESSING                 │
│              │                   │                         │
│              │                   ├─→ SUCCESS               │
│              │                   │   ├─→ VIEWING_RESULTS   │
│              │                   │   ├─→ COMPARING         │
│              │                   │   └─→ EXPORTING         │
│              │                   │       │                 │
│              ├────────────────────────┘  │                 │
│              │                           │                 │
│              └─────────────────────────┘  │                 │
│                                           ↓               │
│                                       IDLE (Ready for new) │
│                                                             │
│              └─→ ERROR_HANDLING ─→ IDLE (Try again)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Database State Changes

```
Step 1: Create Job
  Before: job_postings table is empty
  Action: POST /api/jobs {title, description}
  After:  job_postings.id = UUID (new)
          job_postings.extracted_requirements = {...}

Step 2: Upload Resumes
  Before: candidates table is empty for this job
  Action: POST /api/upload {job_id, files[]}
  After:  candidates.count += 20 (new rows)
          Each with job_id reference

Step 3: Analyze
  Before: job_matches table empty for this job
  Action: POST /api/analyze {job_id}
  After:  job_matches.count += 20 (new rows)
          Each with candidate_id, job_id, match_score, etc.

Step 4: View Results
  Before: Results in DB but not shown to user
  Action: GET /api/results/{job_id}
  After:  Data sorted by rank and returned to frontend
          No DB changes

Step 5: Export
  Before: Results in DB
  Action: GET /api/export/{job_id}?format=csv
  After:  CSV file generated and downloaded
          No DB changes
```

---

## 5. User Persona Flows

### 5.1 Recruiter (Primary User)

**Goal:** Screen 20 resumes quickly  
**Time availability:** 15 minutes

```
0:00 ┌─ Navigates to app
0:05 ├─ Enters job title: "Python Developer"
0:15 ├─ Pastes job description (500 chars)
0:20 ├─ Uploads 20 resumes (drag-drop)
0:25 ├─ Clicks Analyze
0:25 ├─ Sees progress: "Processing..."
2:30 ├─ Results loaded automatically
2:35 ├─ Scans top 5 candidates
2:40 ├─ Clicks "Compare" on top 3
2:50 ├─ Reviews comparison
3:00 ├─ Clicks "Export CSV"
3:05 ├─ CSV downloaded
3:15 └─ Shares with hiring manager
       Time saved: 1.5 hours (vs. manual review)
```

### 5.2 Hiring Manager (Secondary User)

**Goal:** Review candidate comparison  
**Time availability:** 10 minutes

```
0:00 ┌─ Receives CSV from recruiter
0:05 ├─ Opens app (shared link)
0:10 ├─ Views pre-loaded results
0:15 ├─ Clicks on top candidate for details
1:00 ├─ Reviews matched vs. missing skills
1:05 ├─ Discusses with recruiter: "Good, call John Doe"
1:10 └─ Makes hiring decision

Note: This user doesn't upload/analyze; just reviews results
```

### 5.3 HR Manager (Tertiary User)

**Goal:** Create job posting, monitor hiring pipeline  
**Time availability:** 30 minutes (recurring)

```
0:00 ┌─ Creates new job posting
0:10 ├─ Copies job description from HRIS
0:20 ├─ Saves job posting
0:25 ├─ Scheduler: "Analysis created, ready for resumes"
2:00 ├─ (Recruiter uploads resumes)
      ├─ (Auto-analyzed)
2:30 ├─ Views analytics dashboard (future)
      ├─ "Python Developer: 92% best match"
2:40 ├─ Approves candidate submission
2:45 └─ Schedules interview

Note: Workflow is more about tracking than detailed analysis
```

---

## 6. Error Scenarios & Recovery

### 6.1 Network Error During Upload
```
User Context:
  ├─ Uploading 20 files over slow WiFi
  ├─ Upload 60% complete
  ├─ Connection drops

Experience:
  ├─ Upload pauses
  ├─ Notification: "Connection lost. Click to retry."
  ├─ Retry button appears
  ├─ User clicks "Resume Upload"
  ├─ Resumes 15 files remaining
  └─ Completes successfully

Backend Behavior:
  ├─ Tracks uploaded chunks
  ├─ Resume from last complete chunk
  └─ No duplicate files in database
```

### 6.2 Claude API Rate Limit
```
User Context:
  ├─ Analyzing 2nd batch of 50 resumes within 1 hour
  ├─ Hits API rate limit

Experience:
  ├─ Progress page shows: "Rate limit reached, waiting..."
  ├─ Automatic retry with exponential backoff
  ├─ "Resuming in 30 seconds..."
  ├─ Resumes automatically
  └─ Results displayed when complete

Backend Behavior:
  ├─ Catches 429 error from Claude
  ├─ Waits 30 seconds
  ├─ Retries failed extractions
  ├─ Logs rate limit event
  └─ No data lost
```

### 6.3 Database Connection Lost
```
User Context:
  ├─ Results page is loading
  ├─ Database connection fails

Experience:
  ├─ Error page: "Unable to load results. Please try again."
  ├─ Retry button available
  ├─ User clicks Retry
  └─ Results load successfully (DB recovered)

Backend Behavior:
  ├─ Connection pool handles reconnection
  ├─ Automatic retry (3 attempts)
  ├─ Error logged
  └─ User can retry from frontend
```

---

## 7. Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    USER INTERACTIONS                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Upload Resume Files ──→ [File Validation]                  │
│  (PDF, DOCX, TXT)      ├─ Check MIME type                   │
│                        ├─ Check file size                   │
│                        └─ Store temporarily                 │
│                                                              │
│                        ↓                                     │
│                                                              │
│  [Text Extraction]                                           │
│  ├─ PDF → PyPDF2 → OCR (if needed)                          │
│  ├─ DOCX → python-docx                                      │
│  └─ TXT → Read directly                                     │
│                                                              │
│                        ↓                                     │
│                                                              │
│  [Claude Skill Extraction]                                   │
│  ├─ Send resume text to Claude API                          │
│  ├─ Claude returns: {technical, soft, certs, etc.}         │
│  └─ Store in database                                       │
│                                                              │
│                        ↓                                     │
│                                                              │
│  [Matching & Ranking]                                        │
│  ├─ Compare candidate skills ← job requirements             │
│  ├─ Calculate match score                                   │
│  ├─ Sort by score                                           │
│  └─ Store results                                           │
│                                                              │
│                        ↓                                     │
│                                                              │
│  [Results Display]                                           │
│  ├─ Frontend queries results API                            │
│  ├─ Display ranked list                                     │
│  └─ Show matched/missing skills                             │
│                                                              │
│                        ↓                                     │
│                                                              │
│  User Actions:                                               │
│  ├─ View Details → [Claude Summary Generation]             │
│  ├─ Compare → [Generate Comparison]                         │
│  └─ Export → [Format as CSV/PDF]                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. Time Benchmarks per Flow

### 8.1 Happy Path Timeline

| Step | Component | Time | Total |
|------|-----------|------|-------|
| Home page load | Frontend | 2s | 2s |
| Input job description | User | 3min | 3min |
| Upload 20 resumes | Network + Frontend | 2min | 5min |
| Text extraction | Backend | 20s | 5m 20s |
| Skill extraction (Claude) | Claude API | 2min | 7m 20s |
| Matching & ranking | Backend | 30s | 7m 50s |
| Results display | Frontend | 2s | 7m 52s |
| Review top 5 candidates | User | 3min | 10m 52s |
| Compare 2 candidates | Frontend | 1s | 10m 53s |
| Export CSV | Backend + Download | 3s | 10m 56s |

**Total Time: ~11 minutes**

### 8.2 Performance SLA

```
SLA Targets:
├─ File upload: 90% complete within 2 minutes (20 files)
├─ Skill extraction: 90% complete within 2 minutes (20 resumes)
├─ Ranking: 100% complete within 1 minute
├─ Results display: Load within 2 seconds
├─ API response: <500ms (excluding Claude processing)
└─ Database query: <100ms
```

---

## 9. Accessibility Flows

### 9.1 Keyboard Navigation
```
Tab through:
1. Job title input
2. Job description textarea
3. Create Job button
4. Upload area (focusable)
5. Browse button
6. Analyze button
7. Results list (keyboard scrollable)
8. Candidate cards (expandable with Enter)
9. Export buttons
```

### 9.2 Screen Reader
```
Announcements:
├─ "Recruitment Intelligence Engine application"
├─ "Upload resumes section"
├─ "Selected 5 files"
├─ "Analyzing candidates, 45% complete"
├─ "Results loaded, 20 candidates ranked"
├─ "Candidate #1: John Doe, 92% match"
└─ "Export options: CSV, PDF"
```

---

## 10. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-22 | Initial tracer document with all user flows |
