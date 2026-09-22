# Memory.md
## Project Context & Memory - Recruitment Intelligence Engine

---

## 1. Project At a Glance

**Project Name:** Recruitment Intelligence Engine (RIE)  
**Purpose:** AI-powered resume screening and candidate ranking system  
**Client/Stakeholder:** HR Teams, Recruiters, Hiring Managers  
**Start Date:** 2026-09-22  
**Target Completion:** Week 6 (MVP)  
**Status:** Planning & Specification Phase  

**Key Success Metrics:**
- MVP completion in 6 weeks
- Resume processing: <3 minutes for 20 files
- Matching accuracy: >85% relevance
- User time saved: 5-10 hours per hire

---

## 2. What This Project Does (One-Liner Summary)

Upload resumes and a job description → AI extracts skills → Ranks candidates by match → Shows matched/missing skills.

**Example:**
```
Input:  5 Python developer resumes + Python Developer job description
Output: Ranked list showing each candidate's skills match with scores
        (Candidate 1: 92% match - has Python, FastAPI, PostgreSQL)
        (Candidate 2: 78% match - has Python, missing FastAPI)
```

---

## 3. Three Core Problems We're Solving

### Problem 1: Time-Consuming Manual Review
**Current:** Recruiters spend 5-10 hours reading each batch of 20 resumes  
**Solution:** Automated text extraction + AI skill matching = 11 minutes total

### Problem 2: Inconsistent Skill Identification
**Current:** Different reviewers identify different skills from same resume  
**Solution:** Claude consistently extracts and categorizes all skills

### Problem 3: Subjective Candidate Ranking
**Current:** "My gut feeling" = subjective, high risk of missing good candidates  
**Solution:** Quantitative match score (0-100%) based on skill alignment

---

## 4. Technology Decisions (Non-Negotiable)

```
Frontend:  Next.js 14 + TypeScript + Tailwind CSS
Backend:   Python 3.10 + FastAPI + SQLAlchemy
Database:  PostgreSQL 14
LLM:       Anthropic Claude Opus 4.1
Storage:   Local filesystem (MVP) / AWS S3 (production)
Deploy:    Vercel (frontend) + Railway/Render (backend)
```

**Why these choices?**
- Next.js: Fast to build, great DX, easy deployment
- FastAPI: Python = better NLP/text processing, fast async framework
- PostgreSQL: Proven, reliable, good for structured data
- Claude: Best at semantic understanding of resumes/skills
- Local storage: MVP doesn't need cloud complexity

---

## 5. Project Scope (What's Included)

### MVP (Weeks 1-6): ✅ MUST HAVE

- [x] Resume upload (PDF, DOCX, TXT)
- [x] Job description input (text paste)
- [x] AI skill extraction (from both resumes & job desc)
- [x] Candidate matching algorithm
- [x] Ranking system (0-100 match score)
- [x] Results dashboard with ranked candidates
- [x] Show matched/missing skills with badges
- [x] Side-by-side candidate comparison
- [x] Export results as CSV

### NOT in MVP (Future Phases)

- ❌ ATS integration
- ❌ Video resume analysis
- ❌ Interview scheduling
- ❌ Offer letter generation
- ❌ Multi-language support
- ❌ User authentication (assumed single user for MVP)
- ❌ Advanced analytics dashboard
- ❌ Team collaboration features

---

## 6. Data Models at a Glance

### Candidates Table
```
id (UUID)
↓
job_id (FK to job_postings)
↓
filename (original file name)
original_text (extracted resume text)
extracted_skills (JSON: technical, soft, certs, languages, frameworks)
experience_years (integer)
certification_count (integer)
created_at, updated_at
```

### Job Postings Table
```
id (UUID)
↓
title (e.g., "Python Developer")
description (full job description text)
extracted_requirements (JSON: required_skills, years_exp, seniority, etc.)
required_years_experience (integer)
seniority_level (string)
created_at
```

### Job Matches Table (Results)
```
id (UUID)
↓
candidate_id (FK)
job_id (FK)
match_score (0-100 float)
matched_skills (JSON array: ["Python", "FastAPI"])
missing_skills (JSON array: ["AWS"])
extra_skills (JSON array: ["Java", "React"])
assessment (text summary)
rank (1, 2, 3, etc.)
created_at
```

---

## 7. Critical User Flows to Remember

### Flow 1: Job Creation
```
User Input: Title + Description
  ↓
Claude Extracts: Required skills, years exp, seniority
  ↓
Stored in DB: job_postings table
  ↓
Ready for: Resume uploads
```

### Flow 2: Resume Upload & Processing
```
User Action: Drag-drop or browse resumes
  ↓
Backend: Validates (MIME type, size < 10MB)
  ↓
Backend: Extracts text (PyPDF2, python-docx, or plain read)
  ↓
Claude: Extracts skills from resume text
  ↓
Stored in DB: candidates table with extracted_skills
  ↓
Ready for: Matching
```

### Flow 3: Analysis & Ranking
```
User Action: Clicks "Analyze"
  ↓
Backend: Loads all candidates + job requirements
  ↓
For Each Candidate:
  ├─ Compare skills against job requirements
  ├─ Calculate match_score using formula
  ├─ Identify matched/missing/extra skills
  └─ Store in job_matches table
  ↓
Sort by match_score DESC
  ↓
Frontend: Display ranked list with visual badges
```

### Flow 4: Results Display
```
Results Page Loads
  ↓
Show Ranked Candidates (1-20):
  ├─ Name & filename
  ├─ Match score (92%, 85%, etc.)
  ├─ Visual progress bar
  ├─ Green badges: Matched skills
  ├─ Red badges: Missing skills
  └─ [View Details] button
  ↓
User Actions:
  ├─ Click candidate for detail view
  ├─ Select 2-3 for comparison
  └─ Export as CSV
```

---

## 8. Key Algorithms Explained

### Match Score Calculation
```
Technical Match = (Matched Technical Skills / Required Technical Skills) × 100
Experience Match = min(Candidate Years / Required Years, 1.0) × 100
Soft Skills Match = (Matched Soft Skills / Required Soft Skills) × 100

Overall = (Tech × 0.5) + (Experience × 0.3) + (Soft × 0.2)

Penalties:
- Each missing critical skill: -10 points
- Each missing nice-to-have: -2 points

Final Score = max(0, Overall - Penalties)
```

**Example:**
```
Candidate: Python ✓, FastAPI ✓, PostgreSQL ✓, AWS ✗, Docker ✗
Job Requires: Python, FastAPI, PostgreSQL, AWS, Docker

Tech Match = 3/5 × 100 = 60%
Experience Match = 5/5 × 100 = 100% (meets requirement)
Soft Skills Match = 100% (both have required soft skills)

Overall = (60 × 0.5) + (100 × 0.3) + (100 × 0.2) = 30 + 30 + 20 = 80%
Penalties = 2 missing × 10 = -20 points
Final = 80 - 20 = 60% (but capped to reasonable range: 65%)
```

### Skill Extraction via Claude

**Strategy:** Use Claude to semantically understand resumes, not regex/keywords
```
Send Resume Text → Claude → Parse JSON → Store in Database

Why Claude?
├─ Understands context ("Python" not same as "Snake" language)
├─ Deduplicates: "Python 3" = "Python" = "Python 3.10"
├─ Categorizes: Technical vs Soft vs Certifications
├─ Handles variations: "Leadership" = "Team Lead" = "Led team of 5"
└─ Extracts years of experience contextually
```

---

## 9. API Endpoints Quick Reference

### Job Management
```
POST /api/jobs
  ├─ Input: {title, description}
  └─ Output: {job_id, extracted_requirements}

GET /api/jobs/{job_id}
  └─ Output: Job details + extraction status
```

### Resume Management
```
POST /api/upload
  ├─ Input: job_id + files (multipart/form-data)
  └─ Output: {uploaded_count, errors[]}

GET /api/candidates/{job_id}
  └─ Output: List of uploaded candidates
```

### Analysis
```
POST /api/analyze/{job_id}
  ├─ Process: Compares all candidates vs job
  └─ Output: Stores results in job_matches table

GET /api/results/{job_id}
  ├─ Output: Ranked candidates with match scores
  └─ Sorted by: match_score DESC
```

### Export
```
GET /api/export/{job_id}?format=csv
  ├─ Output: CSV file with candidates + scores
  └─ Format: rank, name, filename, match_score, skills
```

---

## 10. Claude AI Integration Points

### Where Claude is Used

1. **Skill Extraction from Resume**
   - Input: Resume text (2-5 pages)
   - Output: JSON with technical, soft, certs, languages, frameworks
   - Model: claude-opus-4-1-20250805
   - Tokens: ~300-500 per resume

2. **Job Requirement Extraction**
   - Input: Job description text
   - Output: JSON with required skills, years exp, seniority
   - Model: claude-opus-4-1-20250805
   - Tokens: ~400-600 per job

3. **Matching & Assessment (Optional)**
   - Input: Candidate skills + Job requirements
   - Output: JSON with match score breakdown + brief assessment
   - Model: claude-opus-4-1-20250805
   - Tokens: ~200-300 per comparison

### Prompting Strategy

**Rule 1:** Always return JSON only (no markdown, no explanations)
**Rule 2:** Be specific about required fields in response
**Rule 3:** Use temperature=0 for deterministic outputs
**Rule 4:** Always catch and validate JSON parsing

Example Prompt Structure:
```python
message = client.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1000,
    temperature=0,  # Deterministic
    messages=[{
        "role": "user",
        "content": f"""Extract skills from resume:

{resume_text}

Return ONLY valid JSON:
{{
  "technical_skills": ["skill1"],
  "soft_skills": ["skill1"],
  "years_experience": 5
}}"""
    }]
)
```

---

## 11. File Processing Pipeline

### Step 1: Validation
```
Check: MIME type in {application/pdf, application/vnd.openxmlformats.../docx, text/plain}
Check: File size < 10 MB
Check: Not empty (> 0 bytes)
```

### Step 2: Text Extraction
```
If PDF:
  ├─ Use PyPDF2 to extract text
  ├─ If extraction < 50 chars (scanned PDF):
  │  └─ Use Tesseract OCR
  └─ Store extracted text

If DOCX:
  ├─ Use python-docx to read paragraphs
  └─ Store extracted text

If TXT:
  ├─ Read file directly (UTF-8)
  └─ Store extracted text
```

### Step 3: Cleanup
```
Remove extra whitespace
Remove special characters (keep alphanumeric + common symbols)
Normalize line breaks
Validate length (100 chars minimum, 100k chars maximum)
```

### Step 4: Store
```
INSERT into candidates:
  ├─ job_id (FK from job)
  ├─ filename (original)
  ├─ original_text (extracted)
  ├─ extracted_skills (will be filled next)
  └─ created_at
```

---

## 12. Performance Targets vs Reality

### Targets
```
Skill extraction: 30s per resume (Claude API call)
Ranking 20 candidates: <60s (20 × ~2s per comparison)
Results display: <2s (database query + frontend render)
Total pipeline: <3 minutes for 20 resumes
```

### Reality Check
```
Actual bottleneck: Claude API latency
├─ Network roundtrip: ~2-3s per request
├─ Claude processing: ~5-10s per resume
└─ Total: 7-13s per resume × 20 = 140-260s

Optimization: Batch requests
├─ Send 3-5 resumes in single prompt
├─ Claude processes in parallel internally
└─ Saves ~50% time
```

---

## 13. Common Mistakes to Avoid

### ❌ Mistake 1: Processing Resumes Without AI
**Wrong:** Try to extract skills with regex: `["Python", "Java", "React"]`
**Right:** Use Claude to understand context and deduplicate

### ❌ Mistake 2: Storing Full Files Permanently
**Wrong:** Save all uploaded PDFs forever
**Right:** Extract text → Delete file after 24 hours

### ❌ Mistake 3: Exact String Matching on Skills
**Wrong:** "Python" ≠ "python" in comparison
**Right:** Normalize all skills to lowercase during comparison

### ❌ Mistake 4: No Error Handling on Claude API
**Wrong:** If Claude call fails, entire analysis fails
**Right:** Retry with exponential backoff, fallback to simpler extraction

### ❌ Mistake 5: Hardcoding API Keys
**Wrong:** `ANTHROPIC_API_KEY = "sk-..." in code`
**Right:** Use environment variables: `os.getenv('ANTHROPIC_API_KEY')`

### ❌ Mistake 6: Assuming Single-user is Forever
**Wrong:** Skip authentication entirely
**Right:** Build auth-ready APIs (add user_id to tables)

### ❌ Mistake 7: No Database Cleanup
**Wrong:** Data grows forever, no retention policy
**Right:** Delete old data (30-90 days) automatically

---

## 14. Key Decisions Made

| Decision | Choice | Reasoning |
|----------|--------|-----------|
| LLM Model | Claude Opus 4.1 | Best semantic understanding, worth the cost |
| DB | PostgreSQL | Proven, structured data, good ORM support |
| File Formats | PDF, DOCX, TXT | Covers 99% of resume formats |
| Max Batch Size | 50 resumes | Balances processing time vs. practical use |
| Retention | 30 days | Comply with privacy, don't need forever |
| Match Formula | 0.5 tech, 0.3 exp, 0.2 soft | Tech skills most important for tech roles |
| Auth | None (MVP) | Single user assumption, add later |
| Deployment | Vercel + Railway | Fast, easy, cost-effective for MVP |

---

## 15. Success Criteria (Definition of Done)

### MVP is Done When:

1. ✅ User can upload 1-50 resumes (PDF/DOCX/TXT)
2. ✅ User can enter job description
3. ✅ System extracts skills from both resumes & job
4. ✅ System ranks candidates 1-50 by match score
5. ✅ Results show matched (green) and missing (red) skills
6. ✅ Can compare 2-3 candidates side-by-side
7. ✅ Can export results as CSV
8. ✅ Processing time: <3 minutes for 20 resumes
9. ✅ No unhandled errors (all errors caught & logged)
10. ✅ Responsive design (works on mobile/tablet/desktop)
11. ✅ README with setup instructions
12. ✅ Database migrations included
13. ✅ Tests: 80%+ coverage on business logic

---

## 16. Contact & Escalation

**Project Owner:** [Your Name]  
**Technical Lead:** [Lead Name]  
**Questions:** Refer to PRD.md, Rules.md, or TechSpec.md  
**Issues:** Document in GitHub Issues with: Problem → Expected → Actual  

---

## 17. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-22 | Initial memory document for MVP specification |

---

## Quick Checklist for Building

Before starting development, have:
- [ ] PRD.md read and understood
- [ ] TechSpec.md reviewed for architecture
- [ ] Rules.md bookmarked for reference
- [ ] Tracer.md consulted for user flows
- [ ] Database schema created
- [ ] Claude API key configured
- [ ] GitHub repo initialized
- [ ] Local development environment set up
- [ ] First API endpoint working (/health)

Good luck building! 🚀
