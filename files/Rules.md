# Rules.md
## Recruitment Intelligence Engine - Project Rules & Constraints

---

## 1. Code & Architecture Rules

### 1.1 Technology Stack (MUST USE)
```
Frontend: Next.js 14+ with TypeScript
Backend: Python 3.10+ with FastAPI
Database: PostgreSQL 14+
LLM: Anthropic Claude API (claude-opus-4-1-20250805)
File Storage: Local filesystem (MVP) / AWS S3 (production)
Environment: Node.js 18+, Python venv
```

### 1.2 Code Organization

**Frontend Structure:**
```
frontend/
  ├── app/
  │   ├── page.tsx (home)
  │   ├── upload/
  │   ├── results/
  │   └── compare/
  ├── components/
  │   ├── CandidateCard.tsx
  │   ├── ResultsList.tsx
  │   ├── ComparisonView.tsx
  │   └── SkillBadge.tsx
  ├── lib/
  │   ├── api.ts (API client)
  │   └── types.ts (TypeScript interfaces)
  └── styles/
```

**Backend Structure:**
```
backend/
  ├── main.py (FastAPI app)
  ├── routes/
  │   ├── upload.py
  │   ├── analyze.py
  │   └── results.py
  ├── services/
  │   ├── file_processor.py
  │   ├── skill_extractor.py
  │   ├── matcher.py
  │   └── ranker.py
  ├── models/
  │   ├── database.py
  │   └── schemas.py
  ├── utils/
  │   └── claude_client.py
  └── config.py
```

### 1.3 Naming Conventions

**Python:**
- Functions/methods: `snake_case` (e.g., `extract_skills_from_resume`)
- Classes: `PascalCase` (e.g., `ResumeProcessor`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`)
- Private methods: prefix with `_` (e.g., `_validate_file`)

**TypeScript/JavaScript:**
- Functions: `camelCase` (e.g., `extractSkills`)
- Components: `PascalCase` (e.g., `CandidateCard`)
- Constants: `UPPER_SNAKE_CASE`
- Hooks: prefix with `use` (e.g., `useUploadResume`)

**Database:**
- Tables: `snake_case_plural` (e.g., `candidates`, `job_matches`)
- Columns: `snake_case` (e.g., `match_score`)
- Foreign keys: `{table}_id` (e.g., `candidate_id`)

### 1.4 Error Handling

**MUST DO:**
- All API endpoints must return consistent error format:
  ```python
  {
    "error": True,
    "message": "Human-readable error message",
    "code": "ERROR_CODE",
    "details": {}
  }
  ```
- All file uploads must be validated (type, size, content)
- All Claude API calls must have try-catch with retry logic
- All database operations must handle connection failures

**MUST NOT:**
- Expose internal error messages to frontend
- Return 500 without logging the actual error
- Process files without validation
- Make API calls without timeout

### 1.5 API Endpoint Standards

**Request/Response Format:**
```python
# Request body
{
  "field_name": "value",  # snake_case
  "is_required": true     # boolean
}

# Success response (2xx)
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}

# Error response (4xx, 5xx)
{
  "error": true,
  "code": "ERROR_CODE",
  "message": "Error description",
  "details": { ... }
}
```

**Response Codes:**
- 200: Success
- 201: Created
- 400: Bad request (validation error)
- 413: File too large
- 422: Unprocessable entity (invalid format)
- 429: Rate limit exceeded
- 500: Server error

---

## 2. Data Handling Rules

### 2.1 File Processing

**MUST:**
- Validate file type before processing
- Check file size (max 10MB per file)
- Extract text reliably from PDF, DOCX, TXT
- Handle OCR for scanned PDFs
- Clean and normalize extracted text
- Store original filename and metadata

**MUST NOT:**
- Store files longer than 24 hours (MVP)
- Process without virus/malware scan (production)
- Expose file paths to frontend
- Trust file extension alone (verify MIME type)

**Supported Formats:**
```
PDF:   application/pdf, .pdf
DOCX:  application/vnd.openxmlformats-officedocument.wordprocessingml.document, .docx
TXT:   text/plain, .txt
```

### 2.2 Data Storage (MVP)

**Database:**
- PostgreSQL only (no SQLite, no NoSQL for MVP)
- Use SQLAlchemy ORM for queries
- All sensitive data encrypted at rest
- Implement soft deletes (use `deleted_at` timestamp)

**Data Retention:**
- Candidate data: Keep for 30 days, then delete
- Analysis results: Keep for 90 days, then delete
- Uploaded files: Delete after extraction (24 hours max)

**Backup:**
- Daily automated backups
- Backup retention: 30 days
- Test restore procedures weekly

### 2.3 API Rate Limiting

**Claude API:**
- Respect Anthropic rate limits
- Implement exponential backoff on 429
- Log all API calls for monitoring
- Cache identical requests when possible

**Endpoint Rate Limits (per user, MVP single-user):**
- Upload: 10 requests/minute
- Analyze: 5 requests/minute
- Other: 30 requests/minute

---

## 3. LLM Integration Rules

### 3.1 Claude API Usage

**MUST:**
- Always specify `model: "claude-opus-4-1-20250805"`
- Always set `max_tokens` (use 1000-2000 for most tasks)
- Always use `temperature: 0` for deterministic outputs
- Always validate JSON response from Claude
- Always handle API errors gracefully
- Always log all API calls (for debugging and cost tracking)

**MUST NOT:**
- Use free tier or older models
- Make unbounded API calls
- Retry indefinitely without cap
- Send raw user input without sanitization

### 3.2 Prompting Standards

**Skill Extraction from Resume:**
```python
# System prompt
system_message = """You are an expert recruiter analyzing resumes.
Extract all skills from the provided resume.
Return ONLY valid JSON, no markdown, no explanations.
Do not include soft skills like "hardworking" or "punctual"."""

# User message template
user_message = f"""Extract skills from this resume.
Categorize as: technical, soft, certifications, languages, frameworks.

Resume:
{resume_text}

Return ONLY JSON with this structure:
{{
  "technical": ["skill1", "skill2"],
  "soft": ["skill1"],
  "certifications": ["cert1"],
  "languages": ["language1"],
  "frameworks": ["framework1"]
}}"""
```

**Job Requirement Extraction:**
```python
system_message = """You are an expert HR analyst.
Extract key requirements from job descriptions.
Be precise and extract only stated requirements, not assumptions.
Return ONLY valid JSON, no markdown."""

user_message = f"""Extract requirements from this job posting.

Job Description:
{job_description}

Return JSON with this structure:
{{
  "required_technical_skills": ["skill1", "skill2"],
  "required_soft_skills": ["skill1"],
  "nice_to_have": ["skill1"],
  "years_experience": 5,
  "seniority_level": "mid-level",
  "certifications": []
}}"""
```

**Candidate Matching:**
```python
system_message = """You are an expert in evaluating candidate-job fit.
Compare candidate skills to job requirements.
Be objective and precise in your assessment.
Return ONLY valid JSON, no markdown."""
```

---

## 4. Frontend Rules

### 4.1 UI Components

**MUST:**
- Use React functional components with hooks
- Prop types: Use TypeScript interfaces (no PropTypes)
- Handle loading states (show spinner during processing)
- Handle error states (show error message, retry button)
- Responsive design (mobile, tablet, desktop)
- Accessible (ARIA labels, keyboard navigation)

**MUST NOT:**
- Use class components
- Use inline styles (use CSS modules or Tailwind)
- Render without loading state
- Show raw error messages to users
- Assume screen size

### 4.2 Form Handling

**MUST:**
- Validate input on change (real-time feedback)
- Show validation errors clearly
- Disable submit button during processing
- Show loading indicator during submission
- Success message on completion
- Clear form after successful submission (optional)

**File Upload:**
```typescript
// MUST support
- Drag and drop
- Click to browse
- Multiple file selection
- Progress indicator
- File list (before upload)
- Cancel option
- Error handling for invalid files
```

### 4.3 Results Display

**MUST:**
- Show results in ranked order
- Display match score prominently (percentage + visual bar)
- Use color coding (green=matched, red=missing, gray=extra)
- Make skills clickable/expandable for details
- Show loading state while processing
- Handle empty state (no results)

**MUST NOT:**
- Show raw JSON to users
- Truncate skill names without indication
- Assume single-row display works for all screen sizes
- Show errors without actionable next steps

---

## 5. Testing Rules

### 5.1 Test Coverage (MUST)
- Unit tests: 80%+ coverage for business logic
- Integration tests: Key API workflows
- E2E tests: User flows (upload → analyze → compare)

### 5.2 Test Files
```
backend/
  tests/
    test_file_processor.py
    test_skill_extractor.py
    test_matcher.py
    test_ranker.py
    test_routes.py

frontend/
  __tests__/
    components/
    lib/
    pages/
```

### 5.3 Running Tests
```bash
# Backend
pytest --cov=backend tests/

# Frontend
npm run test -- --coverage
```

---

## 6. Security Rules

### 6.1 Input Validation

**MUST:**
- Validate all file uploads (type, size, content)
- Sanitize all text inputs
- Escape special characters in JSON responses
- Never trust client-side validation alone
- Rate limit API endpoints

**MUST NOT:**
- Execute user input as code
- Store unencrypted sensitive data
- Log user data or file contents
- Allow arbitrary file paths

### 6.2 API Security

**MUST:**
- Use HTTPS only (production)
- Implement CORS properly
- Validate API request signatures (future)
- Use environment variables for secrets
- Never commit `.env` files

**MUST NOT:**
- Expose API keys in frontend code
- Log sensitive data
- Allow direct database access from frontend

### 6.3 Data Privacy

**MUST:**
- Delete uploaded files after extraction
- Don't share data across job analyses
- Encrypt sensitive fields in database
- Have clear data retention policy

---

## 7. Performance Rules

### 7.1 Response Time Targets
- File upload: <5 seconds for 50 MB total
- Skill extraction: <2 minutes for 20 resumes
- Ranking: <30 seconds for 20 candidates
- API response: <1 second (excluding AI processing)

### 7.2 Optimization

**MUST:**
- Cache Claude responses when possible
- Batch API calls intelligently
- Use connection pooling for database
- Compress responses (gzip)
- Lazy load UI components

**MUST NOT:**
- Make unnecessary API calls
- Block user interactions
- Store uncompressed files
- Query entire tables without pagination

---

## 8. Documentation Rules

### 8.1 Code Comments

**MUST:**
- Comment complex algorithms
- Document edge cases
- Explain "why" not "what"
- Keep comments updated with code

**MUST NOT:**
- Over-comment obvious code
- Leave outdated comments
- Comment every line

### 8.2 README Files

Each component folder MUST have:
```
README.md
├── What it does
├── How to use
├── API endpoints (if applicable)
├── Example usage
└── Known limitations
```

### 8.3 API Documentation

Use OpenAPI/Swagger:
- Document all endpoints
- Include request/response examples
- List all error codes
- Specify authentication (if any)

---

## 9. Environment & Deployment

### 9.1 Environment Variables

**Backend (.env):**
```
ANTHROPIC_API_KEY=sk-...
DATABASE_URL=postgresql://user:pass@localhost/recruiter
JWT_SECRET=your-secret-key
ENVIRONMENT=development
LOG_LEVEL=INFO
MAX_FILE_SIZE=10485760
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Recruitment Engine
```

### 9.2 Local Development Setup

**MUST include:**
- `docker-compose.yml` for PostgreSQL
- Scripts for database migrations
- Seed data for testing
- Instructions in README

### 9.3 Deployment

**Frontend:**
- Deploy to Vercel (recommended)
- Environment variables configured
- CI/CD pipeline (GitHub Actions)

**Backend:**
- Deploy to Railway, Render, or AWS
- Database auto-backed up
- Environment variables secured
- Health check endpoint: `GET /health`

---

## 10. Git & Version Control

### 10.1 Commit Messages
```
Format: <type>: <subject>

Types: feat, fix, docs, style, refactor, test, chore
Length: 50 chars max for subject
Example: feat: implement skill extraction from resume
```

### 10.2 Branch Strategy
```
main (production)
├── develop (staging)
    ├── feature/resume-upload
    ├── feature/skill-extraction
    └── bugfix/json-parsing
```

### 10.3 Pull Request (PR) Requirements
- One feature per PR
- Tests included
- Documentation updated
- No merge conflicts
- Code review approval required

---

## 11. Monitoring & Logging

### 11.1 Logging Levels

**MUST log:**
- INFO: User actions (upload, analysis started)
- WARNING: Validation failures, API rate limits
- ERROR: Exceptions, failed API calls
- DEBUG: Variables, function calls (dev only)

**MUST NOT log:**
- Passwords, API keys, sensitive data
- Full file contents
- PII (names, emails in logs, except for association)

### 11.2 Monitoring

**MUST track:**
- API response times
- Error rates
- File processing duration
- Claude API usage (cost)
- Database query performance

---

## 12. Constraints Summary (Quick Reference)

| Item | Rule |
|------|------|
| Max resumes per batch | 50 |
| Max file size per resume | 10 MB |
| Processing time target | <3 min for 20 resumes |
| Data retention | 30-90 days |
| Supported formats | PDF, DOCX, TXT |
| Tech stack | Next.js + FastAPI + PostgreSQL |
| LLM | Claude Opus 4.1 |
| Error handling | JSON responses with error codes |
| Rate limiting | 10/min uploads, 5/min analyze |
| Test coverage | 80%+ |
| Response times | <1s API, <2min skill extraction |

---

## 13. Non-Negotiable (MVP Must-Haves)

1. ✅ All files validated before processing
2. ✅ All Claude calls have error handling
3. ✅ All API responses are JSON with error codes
4. ✅ All sensitive data encrypted or deleted
5. ✅ All tests pass before deployment
6. ✅ Frontend is responsive (mobile works)
7. ✅ No hardcoded API keys or secrets
8. ✅ Database migrations included
9. ✅ README with setup instructions
10. ✅ Error messages are user-friendly

---

## 14. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-22 | Initial rules document |
