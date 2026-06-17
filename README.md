## Overview

MatchMatrix transforms the traditionally chaotic process of matching students to academic projects into a streamlined, fair, and transparent system. Instead of relying on email chains, spreadsheets, and first-come-first-served decisions, this application uses proven algorithms and AI to create optimal matches while keeping staff in complete control.

**The problem it solves:**

- Manual matching processes take 8-10 hours of staff time
- Students often miss out on suitable projects due to inconsistent phrasing
- Decision-making lacks transparency, leading to complaints
- No objective way to justify why a student received a particular project

**The solution:**

- Automated matching that runs in minutes with full auditability
- AI-powered semantic skill matching to catch connections humans might miss
- Fairness algorithms (Gale-Shapley) used in high-stakes matching scenarios
- Clear, human-readable explanations for every student assignment
- Staff override capabilities with real-time feedback

---

## Key Features

### For Administrators

- **One-click matching** - Run the complete matching process with a single button
- **Real-time metrics** - View assignment statistics, average match scores, and capacity utilization
- **Visual analytics** - Heatmaps show student-project fit scores; stacked charts break down score components
- **Drag-and-drop overrides** - Manually reassign students with live score updates
- **Smart conflict resolution** - Hungarian algorithm automatically fills remaining slots optimally
- **Conflict detection** - Flags over-capacity projects, unassigned students, and potential mismatches
- **Export capabilities** - Download final assignments as CSV for integration with other systems

### For Supervisors

- **Custom screening questions** - Add project-specific questions to gather additional information
- **AI-enhanced scoring** - Optional AI evaluation of student responses to screening questions

### For Students

- **Personalized match view** - See assigned project with friendly explanation (no raw scores displayed)
- **Top 3 recommendations** - View "Best match," "Strong match," and "Good match" options
- **AI-powered preference extraction** - Free-text interests automatically suggest suitable projects
- **Interactive Q&A** - Answer supervisor screening questions directly in the interface

### Core Technology

- **Semantic skill matching** - Uses sentence-transformers to understand that "ML" and "Machine Learning" are related
- **Gale-Shapley stable matching** - Produces mathematically fair outcomes where no one can improve without harming another
- **AI-generated explanations** - Claude API creates personalized, encouraging match justifications
- **Greedy alternative** - Fairness slider provides a simpler option when needed
- **Responsible AI framework** - Full transparency about data usage and decision-making

---

## How It Works

### Data Input
Two simple CSV tables provide the foundation:

- **Students**: Name, skills, ranked project preferences, optional free-text interests
- **Projects**: Title, required skills, supervisor, capacity

### Match Score Calculation
For every possible student-project pair, a score (0 to 1) combines three weighted components:

- **Skill match** - Overlap between student skills and project requirements
- **Preference match** - How this project ranks on the student's wish list
- **Availability** - Remaining capacity to prevent overloading popular projects

Staff can adjust the weights of these components using intuitive sliders.

### AI Features (Toggleable)

1. **Semantic skill matching** - Understands related terms and synonyms
2. **Gale-Shapley stable matching** - Fair, mathematically proven assignment
3. **AI match explanations** - Claude generates personalized justifications
4. **Free-text preference extraction** - Turns paragraphs into ranked recommendations
5. **Supervisor question scoring** - AI evaluates custom screening responses

### Assignment Process

1. Match score matrix computed for all student-project pairs
2. Optional AI bonuses (from supervisor questions) applied
3. Selected algorithm (Gale-Shapley or greedy) produces final assignments
4. Results displayed with full visual analytics
5. Staff review, override if needed, and export

---

## About

Live demo: https://match-matrix-vk17.streamlit.app/


