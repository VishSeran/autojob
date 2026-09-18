# Autonomous Job Application Agent

An AI-powered autonomous job application assistant built using **LangGraph**, **FastAPI**, **RAG**, and persistent memory.

The system analyzes job descriptions, compares them with a candidate profile, identifies skill gaps, tailors CV content, generates cover letters, prepares interview questions, and tracks job applications through a multi-agent workflow.

---

## Overview

Searching and applying for jobs involves repeatedly analyzing job descriptions, updating CVs, writing cover letters, researching companies, and preparing for interviews.

The **Autonomous Job Application Agent** aims to automate and assist with these repetitive tasks using a coordinated multi-agent AI workflow while keeping important decisions, such as final application submission, under user control.

The system uses specialized AI agents to handle different stages of the job application process.

---

## Key Features

- Job description analysis
- Candidate profile retrieval
- Job-to-profile matching
- Skill gap identification
- CV tailoring
- Cover letter generation
- Application quality review
- Interview question generation
- Persistent candidate memory
- Job application tracking
- Conditional agent routing
- Automatic revision loops
- Human-in-the-loop approval
- RAG-based profile retrieval
- Structured LLM outputs

---

## Multi-Agent Architecture

The initial system consists of several specialized agents.

```text
                     User
                      |
                      v
                Orchestrator
                      |
                      v
              Job Parser Agent
                      |
                      v
              Profile Retriever
                      |
                      v
               Matching Agent
                      |
            +---------+---------+
            |                   |
            v                   v
     Skills Gap Agent      CV Tailoring Agent
                                |
                                v
                          Reviewer Agent
                                |
                     +----------+----------+
                     |                     |
                Needs Revision          Approved
                     |                     |
                     +----> CV Agent       v
                                      Cover Letter
                                          |
                                          v
                                    Human Approval
                                          |
                                          v
                                  Application Tracker
```

---

## LangGraph Workflow

The agent workflow is implemented using **LangGraph**.

```text
START
  |
  v
parse_job
  |
  v
retrieve_profile
  |
  v
match_candidate
  |
  +------ Low Match ------> Save / Stop
  |
  v
tailor_cv
  |
  v
review_cv
  |
  +------ Revision Required ------+
  |                               |
  +-----------------> tailor_cv <-+
  |
  v
generate_cover_letter
  |
  v
human_approval
  |
  v
track_application
  |
  v
END
```

LangGraph provides the workflow with:

- Shared state
- Conditional routing
- Agent loops
- Checkpointing
- Persistent execution
- Human-in-the-loop interaction
- Error handling and retries

---

## Agents

### Job Parser Agent

Extracts structured information from a job description.

Possible extracted information includes:

- Job title
- Company
- Required skills
- Preferred skills
- Experience requirements
- Education requirements
- Responsibilities
- Technologies
- Location
- Employment type

---

### Profile Agent

Retrieves relevant information about the candidate from stored profile data.

This may include:

- Education
- Technical skills
- Work experience
- Projects
- Certifications
- Achievements
- GitHub projects
- Career preferences

---

### Matching Agent

Compares the job requirements with the candidate profile.

Outputs may include:

```json
{
  "match_score": 82,
  "matched_skills": [
    "Python",
    "FastAPI",
    "LangGraph",
    "Docker"
  ],
  "missing_skills": [
    "Kubernetes",
    "AWS"
  ]
}
```

---

### Skills Gap Agent

Identifies important skills requested by employers that are missing or weak in the candidate profile.

Over time, this information can be used to identify recurring skill gaps across multiple job applications.

---

### CV Tailoring Agent

Creates a job-specific CV version using the candidate's real experience and skills.

The agent can modify:

- Professional summary
- Skill ordering
- Project descriptions
- Experience bullet points
- Relevant technologies

The system must not invent qualifications or experience that the candidate does not have.

---

### Reviewer Agent

Evaluates the generated CV against the job description.

The reviewer can check:

- Requirement coverage
- Relevance
- Clarity
- Keyword usage
- Consistency
- Unsupported claims

If the CV does not meet the required quality level, the workflow routes it back to the CV Tailoring Agent.

```text
CV Agent
   |
   v
Reviewer
   |
   +---- Approved ------> Continue
   |
   +---- Rejected ------> CV Agent
```

---

### Cover Letter Agent

Generates a personalized cover letter based on:

- Candidate profile
- Job requirements
- Company
- Relevant projects
- Relevant skills

---

### Interview Preparation Agent

Generates interview preparation material based on the analyzed job.

Examples include:

- Technical questions
- Behavioral questions
- Project-related questions
- Skill-specific questions
- Suggested preparation topics

---

## Memory Architecture

The system uses different memory layers rather than storing everything as simple conversation history.

```text
                     Agent System
                          |
        +-----------------+-----------------+
        |                 |                 |
        v                 v                 v

  Working Memory     Semantic Memory    Application Memory

Current workflow     CV embeddings       Job applications
Current job          Projects            Status
Agent state          Skills              Companies
Temporary data       Experience          Interviews
```

### Working Memory

Stores temporary information required during the current LangGraph execution.

### Semantic Memory

Stores searchable candidate information such as:

- CV content
- Projects
- Skills
- Certifications
- Previous experience

A vector database can be used for semantic retrieval.

### Application Memory

Stores structured information about previous job applications.

Example:

```text
Company: Example AI
Role: AI Engineer
Status: Interview
Match Score: 86%
Applied Date: 2026-09-18
```

---

## Technology Stack

### Frontend

- Next.js
- TypeScript
- Tailwind CSS

### Backend

- FastAPI
- Python
- Pydantic

### Agent Framework

- LangGraph
- LangChain

### LLM

Possible providers:

- OpenAI
- Groq
- Anthropic
- Google Gemini

### Database

- PostgreSQL

### Vector Database

Possible options:

- pgvector
- Qdrant
- Chroma

### Memory / Checkpointing

- LangGraph Checkpointer
- PostgreSQL
- Redis

### External Tool Integration

- MCP
- GitHub integrations
- Document parsing tools
- Job search tools

---

## Proposed Project Structure

```text
autonomous-job-application-agent/
│
├── backend/
│   │
│   ├── agents/
│   │   ├── job_parser_agent.py
│   │   ├── profile_agent.py
│   │   ├── matching_agent.py
│   │   ├── skills_gap_agent.py
│   │   ├── cv_agent.py
│   │   ├── reviewer_agent.py
│   │   ├── cover_letter_agent.py
│   │   └── interview_agent.py
│   │
│   ├── workflow/
│   │   ├── graph.py
│   │   ├── state.py
│   │   └── routes.py
│   │
│   ├── schemas/
│   │   ├── job_schema.py
│   │   ├── candidate_schema.py
│   │   ├── match_schema.py
│   │   └── application_schema.py
│   │
│   ├── memory/
│   │   ├── profile_memory.py
│   │   ├── application_memory.py
│   │   └── vector_memory.py
│   │
│   ├── retrievers/
│   │   └── profile_retriever.py
│   │
│   ├── services/
│   │   ├── database_service.py
│   │   └── llm_service.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   └── main.py
│
├── frontend/
│
├── tests/
│
├── docs/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## Workflow State

A simplified LangGraph state may look like:

```python
from typing import TypedDict


class JobApplicationState(TypedDict):

    job_description: str

    job_details: dict

    candidate_profile: dict

    match_score: float

    matched_skills: list[str]

    missing_skills: list[str]

    tailored_cv: dict

    cover_letter: str

    review_feedback: str

    revision_count: int

    approved: bool
```

---

## Development Roadmap

### Phase 1 — Core Agent Workflow

Build the first LangGraph workflow with:

```text
Job Parser
    |
    v
Profile Retriever
    |
    v
Matching Agent
    |
    v
CV Tailoring Agent
    |
    v
Reviewer Agent
```

### Phase 2 — Persistent Memory

Add:

- PostgreSQL
- Candidate profiles
- Application history
- LangGraph checkpointing
- Vector-based profile retrieval

### Phase 3 — Application Assistance

Add:

- Cover Letter Agent
- Skills Gap Agent
- Interview Agent
- Application tracker

### Phase 4 — Tool Integration

Add MCP tools for:

- GitHub profile retrieval
- Portfolio analysis
- Document handling
- Company research
- Job information retrieval

### Phase 5 — Dashboard

Build a dashboard showing:

- Total applications
- Pending applications
- Interviews
- Rejections
- Job match scores
- Frequently requested skills
- Recurring skill gaps

Example:

```text
Applications: 32
Interviews: 6
Pending: 9
Rejected: 17

Most Requested Skills

Python       86%
Docker       71%
AWS          62%
LangGraph    58%
Kubernetes   43%

Recurring Skill Gaps

AWS
Kubernetes
LLMOps
Cloud deployment
```

---

## Future Improvements

Possible future extensions include:

- Automatic job discovery
- Company research agent
- GitHub portfolio analyzer
- Email integration
- Calendar integration
- Interview scheduling
- Resume version management
- Application analytics
- Skill recommendation system
- Agent observability
- LLM evaluation pipelines
- Multi-user support

---

## Project Goal

The goal of this project is not simply to generate CVs or cover letters.

The main objective is to explore and implement a production-oriented **agentic AI system** using:

- Multi-agent orchestration
- Persistent memory
- RAG
- Tool calling
- Conditional workflows
- Human-in-the-loop systems
- Agent evaluation
- Structured outputs
- MCP integrations
- Long-running AI workflows

---

## Disclaimer

This project is intended to assist users during the job application process.

Generated CV content, cover letters, recommendations, and job analysis should always be reviewed by the user before being submitted to an employer.

The system should never fabricate qualifications, skills, work experience, certifications, or achievements.

---

## License

This project is intended for educational, research, and portfolio purposes.

A suitable open-source license can be added based on the future distribution requirements of the project.
