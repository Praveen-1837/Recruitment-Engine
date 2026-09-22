# Product Requirements Document (PRD)
## AI Recruitment Intelligence Engine

**Project Name:** Recruitment Intelligence Engine  
**Version:** 1.0 MVP  
**Status:** Planning Phase  
**Last Updated:** 2026-09-22

---

## 1. Executive Summary

The Recruitment Intelligence Engine is an AI-powered system that helps HR teams and recruiters make data-driven hiring decisions by automatically analyzing resumes, extracting candidate skills, comparing them against job requirements, and providing ranked candidate lists with detailed skill matching insights.

Instead of manually reviewing resumes, the system:
- Uploads and parses multiple resume formats (PDF, DOCX, TXT)
- Accepts job descriptions as text input
- Uses Claude AI to intelligently extract skills and requirements
- Compares candidates and ranks them by relevance
- Provides visual insights on matched/missing skills

---

## 2. Problem Statement

**Current State:**
- HR teams manually review resumes, a time-consuming process
- No standardized skill extraction or comparison
- Difficult to identify candidates with exact skill matches
- Subjective decision-making based on resume reading
- No quantitative matching score

**Target Users:**
- HR Managers
- Recruiters
- Talent Acquisition Teams
- Company hiring managers

**Pain Points:**
1. Time-consuming manual resume screening
2. Inconsistent skill identification across resumes
3. Difficulty tracking skill gaps
4. No automated candidate ranking
5. Risk of missing qualified candidates

---

## 3. Product Goals

### Primary Goals
1. **Automate Resume Analysis** - Extract structured data from unstructured resume documents
2. **Intelligent Skill Matching** - Use AI to semantically match candidate skills to job requirements
3. **Quantitative Ranking** - Provide objective candidate ranking based on skill alignment
4. **Time Savings** - Reduce resume review time from hours to minutes
5. **Accuracy** - Minimize false negatives in candidate screening

### Secondary Goals
1. Support batch resume processing (5-50 candidates)
2. Provide exportable reports (CSV, PDF)
3. Track hiring metrics and trends
4. Build a reusable skill database

---

## 4. User Stories

### 4.1 Recruiter - Initial Candidate Screening
**As a** recruiter reviewing 20 resumes for a Python Developer role  
**I want** to upload all resumes and get a ranked list of best matches  
**So that** I can focus on top candidates instead of reading every resume  

**Acceptance Criteria:**
- Upload 20 PDF resumes in <30 seconds
- Analyze all resumes in <2 minutes
- Get ranked list with match scores
- See matched and missing skills for each candidate

### 4.2 HR Manager - Job Requirements Input
**As an** HR manager  
**I want** to paste a job description  
**So that** the system understands what skills are required  

**Acceptance Criteria:**
- Paste job description text (no file upload)
- System extracts required/preferred skills
- System identifies seniority level and experience
- Can modify extracted requirements if needed

### 4.3 Hiring Manager - Candidate Comparison
**As a** hiring manager  
**I want** to compare top 3 candidates side-by-side  
**So that** I can see their strengths and weaknesses relative to the role  

**Acceptance Criteria:**
- Side-by-side comparison view
- Visual skill matching (green=match, red=missing)
- Experience level comparison
- Export comparison as PDF

### 4.4 Recruiter - Skill Gap Analysis
**As a** recruiter  
**I want** to see what skills my top candidate is missing  
**So that** I can assess training needs or plan onboarding  

**Acceptance Criteria:**
- Clear list of missing critical skills
- Clear list of bonus/extra skills
- Skills categorized as required vs. nice-to-have

---

## 5. Features & Requirements

### 5.1 Core Features (MVP - Week 1-6)

#### Feature 1: Resume Upload & Processing
- **Description:** Users can upload resumes in multiple formats
- **Formats Supported:** PDF, DOCX, TXT
- **Batch Upload:** Support 1-50 resumes per upload
- **Processing:** Extract text from all formats
- **Validation:** 
  - File size limit: 10MB per file
  - Supported formats validation
  - OCR for scanned PDFs

#### Feature 2: Job Description Input
- **Description:** Input job requirements via text paste
- **Input Method:** Textarea (no file upload)
- **Min Length:** 200 characters
- **Max Length:** 50,000 characters
- **Auto-extract:** System automatically extracts:
  - Required skills (technical & soft)
  - Years of experience
  - Seniority level
  - Nice-to-have skills

#### Feature 3: AI Skill Extraction
- **From Resumes:** Extract:
  - Technical skills (programming languages, tools, frameworks)
  - Soft skills (communication, leadership, teamwork)
  - Certifications and licenses
  - Languages spoken
  - Years of experience in each skill

- **From Job Description:** Extract:
  - Required technical skills
  - Required soft skills
  - Required certifications
  - Minimum years of experience
  - Preferred/nice-to-have skills

#### Feature 4: Candidate Matching & Ranking
- **Matching Logic:**
  - Compare each candidate's skills against job requirements
  - Calculate match score (0-100%)
  - Identify matched skills
  - Identify missing critical skills
  - Identify extra/bonus skills

- **Ranking Criteria:**
  1. Overall match percentage (primary)
  2. Number of matched skills (secondary)
  3. Years of relevant experience (tertiary)

#### Feature 5: Results Dashboard
- **Display:**
  - Ranked candidate list (best to worst)
  - Candidate name & position from resume
  - Match percentage (visual bar + number)
  - Matched skills (green badges)
  - Missing skills (red badges)
  - Experience level indicator

- **Actions:**
  - Click candidate for detailed view
  - Compare 2-3 candidates side-by-side
  - Export results as CSV

#### Feature 6: Candidate Detail View
- **Information:**
  - Full matched skills list
  - Full missing skills list
  - Brief assessment/summary
  - Relevant experience highlights
  - Certifications match

#### Feature 7: Side-by-Side Comparison
- **Support:** Compare 2-3 candidates simultaneously
- **Display:**
  - Skill comparison table
  - Match score comparison
  - Experience comparison
  - Recommendations
  - Export as PDF

### 5.2 Phase 2 Features (Weeks 7+)

- Batch job posting analysis (create once, use for multiple uploads)
- Skill database/glossary (normalize similar skills)
- Soft skill scoring and analysis
- Interview question generation for shortlisted candidates
- Hiring metrics dashboard
- Saved searches and templates
- Team collaboration (share results with hiring managers)
- Feedback loop (mark candidates as hired/rejected, improve algorithm)

---

## 6. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Resume processing speed | <3 mins for 20 resumes | Avg time per batch |
| Matching accuracy | >85% relevance | Manual validation spot checks |
| User time saved | 5-10 hours per hire | Survey after use |
| Candidate drop-off | <5% system errors | Error rate tracking |
| Feature adoption | >70% use comparison view | Usage analytics |

---

## 7. User Flow - Happy Path

```
1. Recruiter lands on home page
   ↓
2. Uploads 20 resumes (drag-drop or browse)
   ↓
3. Pastes job description
   ↓
4. Clicks "Analyze"
   ↓
5. System processes (shows loading spinner)
   ↓
6. Gets ranked list of 20 candidates
   ↓
7. Clicks on top 3 candidates to review skills
   ↓
8. Selects top 2 and clicks "Compare"
   ↓
9. Reviews side-by-side comparison
   ↓
10. Clicks "Export as PDF"
    ↓
11. Downloads and shares with hiring manager
```

---

## 8. Out of Scope (MVP)

The following are NOT included in the MVP but may be added later:

- Applicant Tracking System (ATS) integration
- Video resume analysis
- Salary negotiation tools
- Background check integration
- LinkedIn profile import
- Interview scheduling
- Offer letter generation
- Multiple language support (beyond skill names)
- Advanced ML model training on feedback

---

## 9. Constraints & Assumptions

### Constraints
- MVP must be buildable in 6 weeks
- Single-user system (no authentication yet)
- No persistent data storage required for MVP
- Maximum 50 resumes per batch
- Maximum 100 candidates per job analysis

### Assumptions
- Users provide well-formatted resumes (not hand-written)
- Job descriptions are in English
- All resumes are in English
- Recruiters have basic technical literacy
- Claude API will be available and reliable
- Budget allocated for API usage

---

## 10. Acceptance Criteria - MVP Complete

- [ ] Users can upload 1-50 resumes (PDF, DOCX, TXT)
- [ ] Job description text input works
- [ ] AI extracts skills from both resumes and job description
- [ ] Candidates are ranked by match score
- [ ] Results display matched and missing skills
- [ ] Side-by-side candidate comparison works
- [ ] Results can be exported as CSV
- [ ] System processes 20 resumes in <3 minutes
- [ ] No critical errors in 50 test cases
- [ ] UI is responsive and works on desktop/tablet

---

## 11. Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1: Setup | Week 1-2 | Backend API, file processing, DB schema |
| Phase 2: AI Integration | Week 3-4 | Skill extraction, matching algorithm |
| Phase 3: Ranking | Week 5 | Ranking algorithm, scoring |
| Phase 4: Frontend | Week 6 | UI, upload, results dashboard |
| Phase 5: Testing & Polish | Week 7 | Bug fixes, performance, documentation |

---

## 12. Dependencies

- Anthropic Claude API (for skill extraction & analysis)
- File processing libraries (PyPDF2, python-docx)
- Database (PostgreSQL)
- Web framework (Next.js frontend, FastAPI backend)
- Cloud storage (optional: AWS S3 for files)

---

## 13. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-09-22 | AI | Initial PRD |
| 1.0 | 2026-09-22 | AI | Final MVP scope |
