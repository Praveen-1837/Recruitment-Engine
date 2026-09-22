# Design.md
## UI/UX Design Specifications - Recruitment Intelligence Engine

---

## 1. Design System Overview

### 1.1 Color Palette

**Primary Colors:**
```
Primary Blue:     #0066CC (Actions, CTAs)
Success Green:    #00B359 (Matched skills, success states)
Danger Red:       #D94A45 (Missing skills, errors)
Warning Amber:    #FFB900 (Loading, in-progress)
Neutral Gray:     #F5F5F5 (Backgrounds)
Dark Gray:        #333333 (Text)
White:            #FFFFFF (Cards, backgrounds)
Light Gray:       #CCCCCC (Borders, dividers)
```

**Color Usage:**
```
Matched Skills:  Background: #E8F5E9 (light green), Text: #00B359 (green)
Missing Skills:  Background: #FFEBEE (light red), Text: #D94A45 (red)
Extra Skills:    Background: #F3F3F3 (light gray), Text: #666666 (gray)
Match Score 90%+: #00B359 (green)
Match Score 70-89%: #FFB900 (amber)
Match Score <70%: #D94A45 (red)
```

### 1.2 Typography

**Font Family:** Inter or Segoe UI (system default)

**Font Sizes & Weights:**
```
Page Title (H1):       32px, bold (weight: 700)
Section Title (H2):    24px, semibold (weight: 600)
Card Title (H3):       18px, semibold (weight: 600)
Body Text:             16px, regular (weight: 400)
Small Text:            14px, regular (weight: 400)
Label/Caption:         12px, regular (weight: 400)
Monospace (code):      13px, Courier New or Monaco
```

**Line Height:**
```
H1-H3:  1.3
Body:   1.5
Labels: 1.4
```

### 1.3 Spacing & Layout

**Base Unit:** 8px (all spacing is multiple of 8)

```
Spacing Scale:
xs:  4px  (minimal)
sm:  8px  (padding, margins)
md:  16px (sections, gaps)
lg:  24px (major sections)
xl:  32px (page margins)

Padding (cards):     16px
Padding (inputs):    12px (vertical) × 16px (horizontal)
Margin (blocks):     16px (between major sections)
Border Radius:       8px (cards, buttons)
Border Radius (pill): 24px (badges, pills)
```

**Grid:**
```
Desktop:  12-column grid with 24px gutters
Tablet:   12-column grid with 16px gutters
Mobile:   4-column grid with 8px gutters
Max Width: 1200px (centered with 40px margins)
```

---

## 2. Pages & Screens

### 2.1 Home Page (Landing)

**Layout:** Hero section + Feature cards + CTA

**Components:**
```
┌─────────────────────────────────────────────────┐
│  Logo & Navigation                              │
│  [Home] [Features] [FAQ] [GitHub]               │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│            HERO SECTION                         │
│  "AI Recruitment Intelligence Engine"           │
│  "Upload resumes. Rank candidates. Save time."  │
│                                                  │
│  [Get Started] [View Demo]                      │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  FEATURE CARDS (3 columns)                      │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ 📤 Upload│  │ 🤖 Analyze│  │ 📊 Rank │      │
│  │ Resumes  │  │ Skills   │  │ Candidates
│  │          │  │ with AI  │  │          │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  QUICK STATS                                    │
│  5,000+ resumes analyzed | 98% accuracy        │
│  Average time saved: 8 hours per hire           │
└─────────────────────────────────────────────────┘

Footer: Copyright, Links, Social
```

**Design Notes:**
- Minimal, clean design
- High contrast for accessibility
- Mobile-responsive hero
- Large CTA buttons (minimum 44px height for touch)

### 2.2 Upload Page

**Layout:** Two-column (sidebar + main content)

**Components:**
```
┌──────────────────────────────────────────────────┐
│ Recruitment Engine  [Back]                       │
├──────────────────────────────────────────────────┤
│                                                  │
│  SIDEBAR (Left)          │  MAIN CONTENT        │
│  ─────────────────────   │  ──────────────      │
│  1. Create Job     ✓     │  Step 2:             │
│  2. Upload Files   ⊙     │  Upload Resumes      │
│  3. Review Results        │                     │
│  4. Export               │  Job: Python Dev    │
│                          │  Created: 2 hours   │
│                          │                     │
│                          │  ┌─────────────┐    │
│                          │  │ Drag & drop │    │
│                          │  │ resumes     │    │
│                          │  │ here        │    │
│                          │  │             │    │
│                          │  │ [Browse]    │    │
│                          │  └─────────────┘    │
│                          │                     │
│                          │  File List:         │
│                          │  ✓ john_doe.pdf     │
│                          │  ✓ jane_smith.pdf   │
│                          │  ✓ alex_johnson.pdf │
│                          │  ✓ (17 more files)  │
│                          │                     │
│                          │  [Clear] [Analyze]  │
└──────────────────────────────────────────────────┘
```

**Upload Area:**
- Drag-drop zone: 300px × 200px min
- Accepts: PDF, DOCX, TXT
- Visual feedback on hover: Background changes
- Progress: Horizontal bar showing upload %
- Error handling: Red text below area

**File List:**
- Table with: Filename, Size, Status (✓ or ✗)
- Scrollable if >5 files
- Remove button (×) for each file
- Select all checkbox (optional)

### 2.3 Processing Page

**Layout:** Full-width progress display

**Components:**
```
┌──────────────────────────────────────────────────┐
│ Recruitment Engine  [Back]                       │
├──────────────────────────────────────────────────┤
│                                                  │
│         ANALYZING CANDIDATES                    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ Step 1: Extracting text...      ✓ 100% │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ Step 2: Extracting skills...   ⟳  45% │    │
│  │ Processed: 9/20 resumes                │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ Step 3: Comparing skills...    ⊘   0%  │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  Time Remaining: ~2 minutes                    │
│                                                  │
│  [Cancel Analysis]                              │
│                                                  │
│  You can close this page. We'll notify          │
│  when ready. Or check back in 2 minutes.        │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Design Notes:**
- Show 3 parallel processes
- Animated progress bars
- Each step has status (✓ complete, ⟳ in progress, ⊘ pending)
- Time remaining estimate
- Allow users to leave and return

### 2.4 Results Page

**Layout:** Main content area with sidebar

**Components:**
```
┌──────────────────────────────────────────────────┐
│ Recruitment Engine  [< Back]  [Home] [Export]    │
├──────────────────────────────────────────────────┤
│                                                  │
│  RESULTS SUMMARY (Top)                          │
│  ┌────────────────────────────────────────────┐ │
│  │ Job: Python Developer                      │ │
│  │ Total Candidates: 20 | Time: 2m 34s       │ │
│  │ Best Match: John Doe (92%)                │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  CANDIDATE LIST (Main Area)                     │
│  ┌────────────────────────────────────────────┐ │
│  │ ☑ Rank: 1  John Doe (john_doe.pdf)       │ │
│  │    Match Score:  92%  ████████████░       │ │
│  │    Matched: ✓ Python ✓ FastAPI            │ │
│  │    Missing:  ✗ AWS  ✗ Docker             │ │
│  │    [View Details ▼]                        │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │ ☑ Rank: 2  Jane Smith (jane_smith.pdf)   │ │
│  │    Match Score:  85%  ████████░░░         │ │
│  │    Matched: ✓ Python ✓ PostgreSQL         │ │
│  │    Missing:  ✗ FastAPI  ✗ AWS            │ │
│  │    [View Details ▼]                        │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │ ☑ Rank: 3-20... (similar cards)           │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  PAGINATION                                     │
│  [< Previous] Page 1 of 2 [Next >]              │
│                                                  │
│  BULK ACTIONS                                   │
│  [Compare Selected (0)]  [Export Selected CSV]  │
└──────────────────────────────────────────────────┘
```

**Candidate Card Details:**
```
┌─ Candidate Card ────────────────────────────────┐
│                                                  │
│  ☑  [Avatar] John Doe          file.pdf         │
│                                                  │
│  #1 Match: 92%  ████████████░░░░░░░  (92)      │
│                                                  │
│  Matched Skills (Matched 7 of 8 required):      │
│    ✓ Python        ✓ FastAPI      ✓ Postgres   │
│    ✓ SQLAlchemy    ✓ REST API     ✓ Git        │
│    ✓ Leadership                                 │
│                                                  │
│  Missing Skills (Needed for role):              │
│    ✗ AWS           ✗ Kubernetes                │
│                                                  │
│  Extra Skills (Bonus):                          │
│    + Java          + React        + Docker      │
│                                                  │
│  Experience: 5 years (Meets 5 year requirement) │
│                                                  │
│  Assessment:                                    │
│  "Strong match. Has all core backend skills.   │
│   Missing cloud experience but fundamentals    │
│   are excellent. Would be ready in 3 months."  │
│                                                  │
│  [View Full Resume] [View Details ▼]           │
│                                                  │
└─────────────────────────────────────────────────┘
```

### 2.5 Candidate Detail Modal

**Layout:** Modal overlay, 600px wide

**Components:**
```
┌─────────────────────────────────────────────┐
│ Candidate Details                        ✕   │
├─────────────────────────────────────────────┤
│                                              │
│ John Doe                                    │
│ john_doe.pdf                                │
│                                              │
│ Match Score: 92%  ████████████░  [Excellent]│
│                                              │
│ ─────────────────────────────────────────── │
│                                              │
│ MATCHED SKILLS (7 total)                   │
│ ┌──────────┬──────────┬──────────┐         │
│ │ Python   │ FastAPI  │ Postgres │         │
│ │ Backend  │ Web      │ Database │         │
│ └──────────┴──────────┴──────────┘         │
│ ┌──────────┬──────────┬──────────┐         │
│ │ Git      │ REST API │ Flask    │         │
│ │ VCS      │ API      │ Legacy   │         │
│ └──────────┴──────────┴──────────┘         │
│                                              │
│ MISSING SKILLS (2 total)                   │
│ ┌──────────┬──────────┐                    │
│ │ AWS      │ Docker   │                    │
│ │ Cloud    │ Infra    │                    │
│ └──────────┴──────────┘                    │
│                                              │
│ EXTRA SKILLS                               │
│ Java, React, TypeScript                    │
│                                              │
│ ─────────────────────────────────────────── │
│ Experience: 5 years  |  5 certs            │
│ Seniority: Senior Developer                │
│ ─────────────────────────────────────────── │
│                                              │
│ [Download Resume] [Compare] [Close]       │
└─────────────────────────────────────────────┘
```

### 2.6 Comparison Page

**Layout:** Side-by-side table

**Components:**
```
┌────────────────────────────────────────────────┐
│ Recruitment Engine  [< Back]  [Export PDF]     │
├────────────────────────────────────────────────┤
│                                                │
│ CANDIDATE COMPARISON                          │
│ Python Developer Role                         │
│                                                │
│ ┌─────────────────┬──────────┬──────────┐    │
│ │ Criteria        │ John Doe │ Jane Smth│    │
│ ├─────────────────┼──────────┼──────────┤    │
│ │ Match Score     │   92%    │   85%    │    │
│ │ Rank            │    #1    │    #2    │    │
│ │ Years Exp       │  5 yrs   │  3 yrs   │    │
│ │ Matched Skills  │   7/8    │   5/8    │    │
│ │ Missing Skills  │    2     │    4     │    │
│ │ Extra Skills    │    3     │    1     │    │
│ └─────────────────┴──────────┴──────────┘    │
│                                                │
│ DETAILED SKILL MATRIX                        │
│ ┌──────────────┬──────────┬──────────┐       │
│ │ Required     │ John Doe │ Jane     │       │
│ │ Skills       │          │ Smith    │       │
│ ├──────────────┼──────────┼──────────┤       │
│ │ Python       │    ✓     │    ✓     │       │
│ │ FastAPI      │    ✓     │    ✗     │       │
│ │ PostgreSQL   │    ✓     │    ✓     │       │
│ │ AWS          │    ✗     │    ✗     │       │
│ │ Docker       │    ✓     │    ✗     │       │
│ │ Leadership   │    ✓     │    ✓     │       │
│ └──────────────┴──────────┴──────────┘       │
│                                                │
│ RECOMMENDATION                                │
│ "John Doe is the stronger fit. More         │
│  experienced and has better technical match. │
│  Both are viable, but John is ready to      │
│  contribute immediately."                    │
│                                                │
│ [Share] [Print] [Export CSV] [Export PDF]   │
└────────────────────────────────────────────────┘
```

---

## 3. Component Design Patterns

### 3.1 Buttons

**Primary Button (CTA)**
```
Background: #0066CC
Text: White, 16px bold
Padding: 12px 24px
Border-Radius: 8px
Hover: Background #0052A3
Active: Scale 0.98, box-shadow
Min Width: 44px (touch target)
Disabled: Opacity 0.5, cursor: not-allowed
```

**Secondary Button**
```
Background: Transparent
Border: 2px #0066CC
Text: #0066CC, 16px bold
Padding: 10px 22px
Hover: Background #F0F5FF
```

**Danger Button (Delete, Cancel)**
```
Background: #D94A45
Text: White
Same padding as primary
Hover: Background #B8372F
```

### 3.2 Badges

**Matched Skill Badge**
```
Background: #E8F5E9
Border: 1px #4CAF50
Text: #00B359, 14px
Padding: 6px 12px
Border-Radius: 16px (pill)
Icon (optional): ✓ checkmark
```

**Missing Skill Badge**
```
Background: #FFEBEE
Border: 1px #D94A45
Text: #D94A45, 14px
Padding: 6px 12px
Border-Radius: 16px (pill)
Icon (optional): ✗ cross
```

**Extra Skill Badge**
```
Background: #F3F3F3
Border: 1px #999999
Text: #666666, 14px
Padding: 6px 12px
Border-Radius: 16px (pill)
Icon (optional): + plus
```

### 3.3 Progress Bar

**Match Score Bar**
```
Height: 8px
Background: #E8E8E8
Filled: Gradient based on score
  90-100%: Green (#00B359)
  70-89%:  Amber (#FFB900)
  0-69%:   Red (#D94A45)
Border-Radius: 4px
Width: 100% of container (min 200px)
```

**Upload Progress**
```
Height: 6px
Background: #F0F0F0
Filled: Blue (#0066CC)
Animation: Smooth 0.3s transition
Shows: "45% uploaded"
```

### 3.4 Form Inputs

**Text Input / Textarea**
```
Border: 1px #CCCCCC
Padding: 12px 16px
Font: 16px regular
Border-Radius: 8px
Focus: Border #0066CC (2px), box-shadow blue glow
Disabled: Opacity 0.5, cursor: not-allowed
Error: Border #D94A45, error text below input
```

**Textarea (Job Description)**
```
Min Height: 200px
Max Height: 500px
Overflow: Auto scroll
Resize: Vertical only
Font: Monospace 13px (for pasting)
Placeholder: "Paste full job description..."
```

### 3.5 File Upload Zone

**Drag-Drop Area**
```
Border: 2px dashed #CCCCCC
Background: #FAFAFA
Min Height: 200px
Padding: 32px
Border-Radius: 12px
Text: "Drag & drop resumes here" (center, gray)
```

**On Hover (User Dragging Files)**
```
Border: 2px dashed #0066CC
Background: #F0F5FF
Cursor: Copy
```

**After Files Added**
```
Border: 1px solid #4CAF50
Background: #F1F8F6
Checkmark icon next to files
```

---

## 4. Responsive Design Breakpoints

### Desktop (1200px+)
```
Sidebar width: 250px
Main content: Full width - 250px
Columns: 12 (for grids)
Font scale: 100%
Spacing: Full (24px md, 32px lg)
```

### Tablet (768px - 1199px)
```
Sidebar: Collapse to hamburger menu
Main content: Full width
Columns: 8
Font scale: 95%
Spacing: 16px md, 24px lg
Candidate cards: Stack vertically
```

### Mobile (320px - 767px)
```
No sidebar (drawer menu only)
Full-width cards
Columns: 4
Font scale: 90%
Padding: Reduced (8px, 16px)
Comparison: Scroll horizontal
Progress bars: Smaller but readable
Buttons: Full-width for primary CTA
```

---

## 5. Accessibility Considerations

### 5.1 Color Contrast
```
Text on Background: 4.5:1 ratio (AA standard)
Matched (Green text on white): ✓ Passes
Missing (Red text on white): ✓ Passes
Match score percentages: Dark text on light or vice versa
All badges meet WCAG AA standards
```

### 5.2 Focus States
```
All interactive elements:
├─ Visible focus outline (2px, blue)
├─ Keyboard navigation (Tab order)
├─ Focus visible on all buttons, links, inputs
└─ Focus trap in modals (cannot tab outside)
```

### 5.3 ARIA Labels
```
Upload area: aria-label="File upload zone for resumes"
Match score: aria-label="John Doe has 92 percent match score"
Matched skills: role="list", aria-label="Matched skills"
Missing skills: role="list", aria-label="Missing skills"
Buttons: aria-label="View details for candidate John Doe"
Modals: aria-modal="true", role="dialog"
```

### 5.4 Dark Mode Support
```
Use CSS variables for colors
Automatically adapt to OS setting (prefers-color-scheme)
Manual toggle option (future)
Contrast maintained in dark mode
Text remains readable
```

---

## 6. Loading & Error States

### 6.1 Loading State
```
Skeleton screens: Gray placeholder boxes
Spinner: Rotating circle (0.8s rotation)
Pulse animation: Subtle opacity pulse
Progress bar: Shows % if available
Message: "Loading candidates..." or "Analyzing skills..."
```

### 6.2 Error State
```
Error Modal / Toast:
├─ Red border or background
├─ ✕ Close button
├─ Headline: "Error uploading file"
├─ Description: Clear, actionable message
├─ Action: Retry button or link to docs
└─ Auto-dismiss: After 5 seconds (for success), manual for errors
```

### 6.3 Empty State
```
Illustration: Minimal, 100px
Headline: "No resumes uploaded yet"
Message: "Upload resumes to get started"
CTA: [Upload Resumes] button
```

---

## 7. Animation & Transitions

### 7.1 Page Transitions
```
Fade-in: 0.2s ease-out
Slide-up: 0.3s ease-out (from bottom)
Scale: 0.2s ease-out (cards on hover)
```

### 7.2 Progress Animation
```
Progress bar fill: 0.3s ease
Color transition: 0.4s ease
Percentage number: No animation (instant)
```

### 7.3 Hover & Click
```
Button hover: 0.15s scale + color change
Card hover: 0.2s box-shadow increase
Badge hover: 0.15s background darken
Smooth all transitions (no jarring changes)
```

---

## 8. Export Formats

### CSV Export
```
Columns:
rank, name, filename, match_score, years_exp, 
matched_skills, missing_skills, extra_skills, assessment

Row Example:
1, John Doe, john_doe.pdf, 92, 5, 
"Python; FastAPI; PostgreSQL", "AWS; Docker", 
"Java; React", "Strong match with core skills"
```

### PDF Export (Comparison)
```
Header: Job title, date, analysis summary
Table: Side-by-side candidate comparison
Skills matrix: Detailed matching
Recommendation: Brief assessment
Footer: Page numbers, timestamp
Style: Professional, printable
```

---

## 9. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-22 | Initial design specification |
