# Resume Generator API

<p align="center">Production-ready AI-powered resume generation microservice with Python 3.12 + FastAPI + CrewAI.</p>

![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) ![CrewAI](https://img.shields.io/badge/CrewAI-0.105-FF6B6B?logo=openai&logoColor=white) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT-412991?logo=openai&logoColor=white) ![DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-4053D6?logo=amazondynamodb&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-Production-2496ED?logo=docker&logoColor=white) ![LaTeX](https://img.shields.io/badge/LaTeX-PDF%20Generation-008080?logo=latex&logoColor=white) ![JWT](https://img.shields.io/badge/JWT-Auth-000000?logo=jsonwebtokens&logoColor=white) ![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white) ![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9?logo=python&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
  - [AI-Powered Resume Generation (CrewAI Multi-Agent)](#ai-powered-resume-generation-crewai-multi-agent)
  - [Dual PDF Templates](#dual-pdf-templates)
  - [JWT Authentication](#jwt-authentication)
  - [Resume Management](#resume-management)
  - [Skill Tracking (DynamoDB)](#skill-tracking-dynamodb)
- [Architecture](#architecture)
  - [Layer Diagram](#layer-diagram)
  - [CrewAI Pipeline Detail](#crewai-pipeline-detail)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication-endpoints)
  - [Resume Generator (AI)](#resume-generator-endpoints)
  - [Capybara Resume (Direct PDF)](#capybara-resume-endpoints)
- [Data Models](#data-models)
  - [Input — CV Request](#input--cv-request)
  - [Output — Resume Data](#output--resume-data)
  - [Capybara Resume](#capybara-resume-model)
- [Running Locally (Without Docker)](#running-locally-without-docker)
- [Running with Docker](#running-with-docker)
  - [Development Mode](#development-mode)
  - [Production Mode](#production-mode)
- [Environment Variables](#environment-variables)
- [AWS DynamoDB Tables](#aws-dynamodb-tables)
- [Knowledge Base (CrewAI)](#knowledge-base-crewai)
- [PDF Generation Pipeline](#pdf-generation-pipeline)
- [Testing](#testing)
- [Code References](#code-references)
- [License](#license)
- [Authors](#authors)

---

## Overview

**Resume Generator API** is a **production-ready Python microservice** that uses a **multi-agent AI system (CrewAI)** to automatically generate professional, well-structured resumes from raw user data.

The user provides their personal information, education, work experience, skills, languages, and certifications. A pipeline of three specialized AI agents then processes this data — writing professional bullet points, structuring the output into a clean JSON, and extracting a validated list of skills — producing a polished `ResumeData` object that can be exported to a PDF using LaTeX.

The system also features a second, independent PDF generator called **Capybara Resume**, which renders a more structured, multi-section CV (with project experience, achievements, complementary education, and more) directly from a rich JSON payload, without going through the AI pipeline.

It is designed to run locally using Docker and to be deployed to any containerized cloud environment.

---

## Key Features

### AI-Powered Resume Generation (CrewAI Multi-Agent)

The core of the system is a three-agent pipeline built with **CrewAI** that runs sequentially:

1. **CV Writer Agent** — Takes raw user data and rewrites it in professional, achievement-oriented language. Uses a real-world example CV as a knowledge source to guide writing style. Will never invent skills, roles, or accomplishments not present in the input.
2. **JSON Formatter Agent** — Converts the professionally written text into a strict, well-defined JSON structure ready for frontend consumption or PDF rendering.
3. **Skills Extractor Agent** — Reads the user's data and extracts only skills that are explicitly listed in a validated professional skills catalog (`skills_catalog.txt`). Will never infer or fabricate skills.

This pipeline guarantees:
- No hallucinated content — only data the user provided is used.
- Consistent, structured JSON output on every run.
- A curated skills profile automatically generated for each user.

### Dual PDF Templates

The API exposes two independent PDF generation paths:

| Template | Description |
|---|---|
| **Standard Resume** | AI-generated resume rendered via a single-column LaTeX template. Sections: header, summary, experience, education, skills, languages, certifications. |
| **Capybara Resume** | Rich multi-section LaTeX template supporting work experience, project experience, achievements, complementary education, and languages. Accepts pre-structured JSON with no AI step. |

Both formats are compiled with `pdflatex` (TeX Live, inside Docker) and returned as a downloadable `application/pdf` response. Temporary files are cleaned up automatically after download.

### JWT Authentication

All resume routes are protected with **JWT Bearer tokens**:
- Passwords are hashed at rest using **bcrypt** (via `passlib`).
- Tokens are signed with a configurable secret key using **HS256** (or any supported algorithm).
- Tokens expire after a configurable number of minutes.
- The `OAuth2PasswordBearer` scheme is used, meaning Swagger UI supports bearer token injection for testing.
- All protected routes extract the current user's email from the token payload automatically.

### Resume Management

Users can manage their generated resumes:
- List all resume references (id, filename, created timestamp) stored in their user profile.
- Fetch the full structured data of a specific resume by ID.
- Rename the filename associated with a resume entry.
- Delete resume references from their profile.

### Skill Tracking (DynamoDB)

After each AI-generated resume, the system automatically stores a `SkillEntry` in DynamoDB. This entry records the user's name, contact info, and the extracted skill list — enabling future analytics, talent matching, or recommendation features.

---

## Architecture

### Layer Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                         HTTP Clients                         │
└───────────────────────────────┬──────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────┐
│                     FastAPI Application                       │
│   /api/v1/auth    /api/v1/resume    /api/v1/capybara          │
│                  Controllers (Routing Layer)                  │
└───────┬────────────────────┬──────────────────────┬──────────┘
        │                    │                      │
┌───────▼──────┐  ┌──────────▼──────────┐  ┌───────▼──────────┐
│ AuthService  │  │   ResumeService      │  │CapybaraResumeSvc │
└───────┬──────┘  └────────┬──────┬─────┘  └───────┬──────────┘
        │                  │      │                 │
        │         ┌────────▼──┐ ┌─▼─────────────┐  │
        │         │  CrewAI   │ │  resume_pdf    │  │
        │         │  Pipeline │ │  Generator     │  │
        │         │  (3 Agents│ │  (LaTeX+PDF)   │  │
        │         │   3 Tasks)│ └────────────────┘  │
        │         └────────┬──┘                  ┌──▼───────────┐
        │                  │                     │resume_capybara│
        │                  │                     │Generator      │
        │                  │                     │(LaTeX+PDF)    │
        │                  │                     └───────────────┘
┌───────▼──────────────────▼──────────────────────────────────┐
│                     Repositories                             │
│       UsersRepository  ResumeRepository  SkillsRepository    │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                     AWS DynamoDB                             │
│       users-table      resumes-table      skills-table       │
└─────────────────────────────────────────────────────────────┘
```

### CrewAI Pipeline Detail

```
Input (InputCVRequest)
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  Task 1: generate_cv                                        │
│  Agent:  cv_writer                                          │
│  Input:  personal_data, education, experience, skills,      │
│          languages, certifications, professional_summary    │
│  Output: Professionally written free-text resume            │
│  Knowledge: cv_oraciones_modelo.txt (writing style guide)   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ (free-text resume)
┌─────────────────────────────────────────────────────────────┐
│  Task 2: structure_cv                                       │
│  Agent:  json_formatter                                     │
│  Output: Clean JSON matching ResumeData schema              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ (structured JSON)
┌─────────────────────────────────────────────────────────────┐
│  Task 3: extract_skills                                     │
│  Agent:  skills_extractor                                   │
│  Input:  original user data (all sections)                  │
│  Output: JSON { "skills": ["skill1", "skill2", ...] }       │
│  Knowledge: skills_catalog.txt (validated skills bank)      │
└─────────────────────────────────────────────────────────────┘
        │                       │
        ▼                       ▼
  ResumeData            SkillEntry saved
  stored in              to DynamoDB
  DynamoDB
```

---

## Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| Web Framework | FastAPI 0.115+ |
| ASGI Server | Uvicorn |
| AI Agents | CrewAI 0.105+ |
| LLM | OpenAI GPT (configurable model) |
| Database | AWS DynamoDB (via boto3) |
| Authentication | JWT (python-jose) + bcrypt (passlib) |
| Data Validation | Pydantic v2 |
| PDF Generation | LaTeX (pdflatex / TeX Live) |
| Package Manager | uv (Astral) |
| Containerization | Docker + Docker Compose |
| Linting | Ruff |

---

## Project Structure

```
resume_generator/
├── Dockerfile                        # Production image (Python 3.12 + TeX Live)
├── docker-compose.yml                # Production compose
├── docker-compose.dev.yml            # Development compose (with .env)
├── pyproject.toml                    # Project metadata & dependencies (uv/hatch)
│
├── knowledge/                        # Knowledge base for CrewAI agents
│   ├── cv_oraciones_modelo.txt       # Real-world CV examples (writing guide)
│   ├── skills_catalog.txt            # Validated professional skills bank
│   └── user_preference.txt           # User context for agents
│
└── src/
    ├── main.py                       # FastAPI app entry point
    │
    ├── core/                         # App initialization & shared infrastructure
    │   ├── config.py                 # Settings (pydantic-settings, reads .env)
    │   ├── db_client.py              # DynamoDB resource + table accessors
    │   ├── init_app.py               # FastAPI factory (CORS, OpenAPI, JWT scheme)
    │   └── router.py                 # Root APIRouter (mounts all sub-routers)
    │
    ├── controllers/                  # HTTP routing layer
    │   ├── auth_controller.py        # POST /auth/register, /login, PUT /reset-password
    │   ├── resume_controller.py      # POST /resume/generate, /download-pdf, GET/DELETE/PUT
    │   └── capybara_resume_controller.py  # POST /capybara/download-pdf
    │
    ├── services/                     # Business logic layer
    │   ├── auth_service.py           # Register, login, password reset
    │   ├── resume_service.py         # AI generation, PDF export, CRUD
    │   ├── capybara_resume_service.py# Direct PDF generation with date formatting
    │   └── user_service.py           # User queries
    │
    ├── repositories/                 # Data access layer (DynamoDB)
    │   ├── user_repository.py        # CRUD users + resume references
    │   ├── resume_repository.py      # Insert/get resumes (handles Decimal types)
    │   └── skills_repository.py      # Insert skill entries
    │
    ├── models/                       # Pydantic schemas
    │   ├── cv_schema.py              # InputCVRequest + sub-models (input)
    │   ├── resume_schema.py          # ResumeData, ResumeReference (output)
    │   ├── capybara_resume.py        # CapybaraResume + all sub-models
    │   ├── user_schema.py            # UserDB, UserRegisterRequest, UserLoginRequest
    │   └── skill_entry.py            # SkillEntry (analytics/talent matching)
    │
    ├── dependencies/
    │   └── auth.py                   # OAuth2 Bearer dependency → get_current_user_email
    │
    ├── resume_generator/             # CrewAI multi-agent pipeline
    │   ├── crew.py                   # @CrewBase: agents, tasks, crew assembly
    │   ├── main.py                   # Local runner with sample inputs
    │   └── config/
    │       ├── agents.yaml           # Agent roles, goals, backstories
    │       └── tasks.yaml            # Task descriptions + expected outputs
    │
    ├── generators/                   # PDF rendering engines
    │   ├── resume_pdf/               # Standard AI resume → LaTeX → PDF
    │   │   ├── cv_pdf_generator.py   # Fills template.tex with ResumeData
    │   │   ├── formatter.py          # Section formatters (header, exp, edu…)
    │   │   ├── compile_pdf.py        # pdflatex subprocess runner
    │   │   └── template.tex          # LaTeX master template
    │   └── resume_capybara/          # Capybara resume → LaTeX → PDF
    │       ├── cv_pdf_generator.py   # Fills template with CapybaraResume
    │       ├── formatter.py          # Extended section formatters
    │       ├── compile_pdf.py        # pdflatex subprocess runner
    │       └── template.tex          # Rich multi-column LaTeX template
    │
    └── utils/                        # Shared utilities
        ├── security.py               # bcrypt hash/verify, JWT encode/decode
        ├── json_cleaner.py           # Strips ```json ``` from agent output
        ├── resume_parser.py          # Dict → ResumeData conversion
        ├── resume_reference_builder.py  # Builds ResumeReference with filename
        ├── skills_extractor.py       # Builds SkillEntry from parsed resume + agent output
        └── uuid_generator.py         # uuid4 generator
```

---

## API Endpoints

### Authentication Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | ❌ | Register a new user (email + password). Password is bcrypt-hashed before storage. |
| `POST` | `/api/v1/auth/login` | ❌ | Login with email + password. Returns a JWT access token. |
| `PUT` | `/api/v1/auth/reset-password` | ✅ JWT | Reset password — verifies old password, stores new bcrypt hash. |

**Register / Login Request Example:**
```json
{
  "email": "user@example.com",
  "password": "myPassword123"
}
```

**Login Response:**
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

---

### Resume Generator Endpoints

All endpoints below require `Authorization: Bearer <token>` unless noted.

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/resume/generate` | ✅ | Run the CrewAI pipeline with the provided CV data. Returns the structured `ResumeData` JSON and persists it to DynamoDB. |
| `POST` | `/api/v1/resume/download-pdf` | ❌ | Render a `ResumeData` JSON to PDF using LaTeX. Returns `application/pdf`. File is deleted after download. |
| `GET` | `/api/v1/resume/` | ✅ | List all resume references (id, filename, created_at) for the authenticated user. |
| `GET` | `/api/v1/resume/{resume_id}` | ❌ | Fetch the full `ResumeData` for a given resume ID. |
| `DELETE` | `/api/v1/resume/{resume_id}` | ✅ | Remove a resume reference from the user's profile. |
| `PUT` | `/api/v1/resume/{resume_id}/rename` | ✅ | Rename the filename of a resume entry. |

---

### Capybara Resume Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/capybara/download-pdf` | ❌ | Render a `CapybaraResume` JSON directly to PDF using the Capybara LaTeX template. No AI step. Returns `application/pdf`. |

---

## Data Models

### Input — CV Request

Sent to `POST /api/v1/resume/generate`:

```json
{
  "personalData": {
    "fullName": "Ana María Gutiérrez",
    "email": "ana@example.com",
    "phone": "+591 71234567",
    "linkedin": "https://linkedin.com/in/ana"
  },
  "education": [
    {
      "institution": "Universidad Privada Boliviana",
      "degree": "Ingeniería de Sistemas",
      "startYear": "2018",
      "endYear": "2023",
      "notes": "Graduated with honors"
    }
  ],
  "experience": [
    {
      "projectName": "E-commerce Platform",
      "role": "Backend Developer",
      "achievements": "Reduced API response time by 40%",
      "teamwork": "Led a team of 4 developers",
      "coordination": "Coordinated with product and design",
      "presentation": "Presented results to the CTO"
    }
  ],
  "skills": [
    { "skill": "Python", "level": "Advanced" },
    { "skill": "Docker", "level": "Intermediate" }
  ],
  "languages": [
    { "language": "English", "level": "B2" }
  ],
  "certifications": [
    {
      "course": "AWS Certified Developer",
      "provider": "Amazon",
      "year": "2023",
      "certificate": "https://example.com/cert"
    }
  ],
  "professionalSummary": {
    "summary": "Backend developer with 2+ years of experience building scalable APIs."
  }
}
```

### Output — Resume Data

Returned by `POST /api/v1/resume/generate` and `GET /api/v1/resume/{resume_id}`:

```json
{
  "fullName": "Ana María Gutiérrez",
  "summary": "Backend developer with 2+ years of experience...",
  "contact": {
    "email": "ana@example.com",
    "linkedin": "https://linkedin.com/in/ana",
    "phone": "+591 71234567"
  },
  "education": [
    {
      "institution": "Universidad Privada Boliviana",
      "degree": "Ingeniería de Sistemas",
      "startYear": "2018",
      "endYear": "2023",
      "description": "Graduated with honors"
    }
  ],
  "experience": [
    {
      "company": "E-commerce Platform",
      "position": "Backend Developer",
      "startDate": "2022",
      "endDate": null,
      "responsibilities": [
        "Reduced API response time by 40% through caching optimizations."
      ]
    }
  ],
  "skills": [{ "name": "Python", "level": "Advanced" }],
  "languages": [{ "name": "English", "proficiency": "B2" }],
  "certifications": [{ "name": "AWS Certified Developer", "institution": "Amazon", "year": 2023 }]
}
```

### Capybara Resume Model

Sent to `POST /api/v1/capybara/download-pdf`. Supports richer sections:

```json
{
  "fullName": "John Doe",
  "contact": {
    "email": "john@example.com",
    "linkedin": "https://linkedin.com/in/johndoe",
    "phone": "+1 555-1234",
    "city": "La Paz",
    "country": "Bolivia"
  },
  "education": [
    {
      "institution": "UPB",
      "degree": "Computer Science",
      "relevantEducationData": "GPA 9.5/10",
      "startDate": "2019-01",
      "endDate": "2023-12",
      "city": "Cochabamba",
      "country": "Bolivia"
    }
  ],
  "experience": [
    {
      "company": "Acme Corp",
      "position": "Software Engineer",
      "relevantCompanyData": "Fintech startup",
      "startDate": "2023-01",
      "endDate": null,
      "city": "La Paz",
      "country": "Bolivia",
      "successSentences": [
        "Built a real-time notification system processing 1M events/day."
      ]
    }
  ],
  "projectExperience": {
    "titleSection": "Open Source Projects",
    "experiences": []
  },
  "skills": ["Python", "FastAPI", "Docker"],
  "softwares": ["VS Code", "Postman", "Figma"],
  "languages": [{ "name": "English", "proficiency": "C1", "certification": "IELTS 7.5" }],
  "achievements": [
    {
      "name": "1st Place Hackathon",
      "institution": "UPB",
      "city": "Cochabamba",
      "country": "Bolivia",
      "date": "2022-11"
    }
  ],
  "complementaryEducation": [
    {
      "courseType": "Online Course",
      "courseName": "Machine Learning Specialization",
      "institution": "Coursera",
      "city": "Online",
      "country": "USA",
      "date": "2023-06"
    }
  ]
}
```

> **Note:** `startDate` / `endDate` fields accept ISO 8601 strings, datetimes, or `null` (meaning "present"). The service normalizes all dates to `MM/YYYY` format and sorts experiences from most recent to oldest before rendering.

---

## Running Locally (Without Docker)

### Prerequisites

- Python 3.10 – 3.12
- [uv](https://docs.astral.sh/uv/) installed
- `pdflatex` available in PATH (TeX Live or MiKTeX) for PDF generation
- AWS credentials with access to DynamoDB

### Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd resume_generator

# 2. Create .env file (see Environment Variables section)
cp .env.example .env

# 3. Install dependencies using uv
uv sync

# 4. Run the development server
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base:** http://localhost:8000/api/v1
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health check:** http://localhost:8000/

---

## Running with Docker

The Docker image includes a full **TeX Live** installation, so PDF generation works out of the box without any local LaTeX setup.

### Development Mode

Uses `docker-compose.dev.yml`, which mounts the `.env` file and exposes port `8000`:

```bash
docker compose -f docker-compose.dev.yml up --build
```

This will:
1. Build the image from `Dockerfile` (Python 3.12-slim + TeX Live packages)
2. Install all project dependencies via `uv sync --frozen --no-dev`
3. Start Uvicorn on port `8000`

### Production Mode

```bash
docker compose up --build
```

Uses the pre-built image tag `resume-builder-backend`.

**Build the image manually:**

```bash
docker build -t resume-builder-backend .
```

**Run the container directly:**

```bash
docker run -p 8000:8000 --env-file .env resume-builder-backend
```

---

## Environment Variables

Create a `.env` file at the root of the project with the following variables:

```env
# OpenAI / CrewAI
MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...

# AWS DynamoDB
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
DYNAMODB_USERS_TABLE=resume-users
DYNAMODB_RESUMES_TABLE=resume-data
DYNAMODB_SKILLS_TABLE=resume-skills

# JWT Authentication
JWT_SECRET_KEY=your_super_secret_key_here
JWT_HASH_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `MODEL` | ✅ | — | OpenAI model name used by CrewAI agents (e.g. `gpt-4o-mini`, `gpt-4o`) |
| `OPENAI_API_KEY` | ✅ | — | OpenAI API key |
| `AWS_ACCESS_KEY_ID` | ✅ | — | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | ✅ | — | AWS IAM secret key |
| `AWS_REGION` | ❌ | `us-east-1` | AWS region where DynamoDB tables exist |
| `DYNAMODB_USERS_TABLE` | ✅ | — | DynamoDB table name for users |
| `DYNAMODB_RESUMES_TABLE` | ✅ | — | DynamoDB table name for resumes |
| `DYNAMODB_SKILLS_TABLE` | ✅ | — | DynamoDB table name for skill entries |
| `JWT_SECRET_KEY` | ✅ | — | Secret key for signing JWT tokens |
| `JWT_HASH_ALGORITHM` | ❌ | `HS256` | JWT signing algorithm |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | ❌ | `30` | JWT token lifetime in minutes |

---

## AWS DynamoDB Tables

The project uses three DynamoDB tables. Below are the required primary key configurations:

| Table | Partition Key | Type | Description |
|---|---|---|---|
| Users table | `email` | String | Stores user credentials and list of resume references |
| Resumes table | `id` | String | Stores full structured `ResumeData` JSON |
| Skills table | `id` | String | Stores `SkillEntry` records per generated resume |

> Tables must be created manually in AWS DynamoDB (or via IaC) before running the application. The application does not auto-create tables.

**Sample User item structure (DynamoDB):**
```json
{
  "email": "user@example.com",
  "password": "$2b$12$...",
  "cvs": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "ana_gutierrez_resume_20240301.pdf",
      "created_at": "2024-03-01T12:00:00+00:00"
    }
  ]
}
```

---

## Knowledge Base (CrewAI)

The `knowledge/` directory contains text files used as knowledge sources by the CrewAI agents at runtime:

| File | Used By | Purpose |
|---|---|---|
| `cv_oraciones_modelo.txt` | `cv_writer` agent | Real-world professional CV examples to guide writing style and achievement-sentence structure |
| `skills_catalog.txt` | `skills_extractor` agent | Validated bank of 100+ professional skills (Python, Docker, AWS, Agile, etc.) — agent may ONLY return skills found here |
| `user_preference.txt` | General context | Default user context (name, role, location) used for agent personalization |

The skills catalog enforces strict extraction — if a skill is not in the catalog, the agent must not include it. This prevents skills hallucination and ensures consistent, validated profile data.

---

## PDF Generation Pipeline

Both PDF generators follow the same internal pipeline:

```
1. ResumeData / CapybaraResume (Pydantic model)
        │
        ▼
2. Formatter functions → LaTeX snippets
   (format_header, format_experience, format_education, …)
        │
        ▼
3. Template placeholder replacement
   template.tex with {{ header }}, {{ experience }}, etc.
        │
        ▼
4. compile_latex_to_pdf()
   - Writes .tex to a TemporaryDirectory
   - Runs: pdflatex -interaction=nonstopmode <file.tex>
   - Reads generated .pdf bytes
   - Copies PDF to system temp dir
   - Cleans up the temp compilation directory
        │
        ▼
5. FileResponse(path=..., media_type="application/pdf")
   + BackgroundTask(os.remove) — deletes file after download
```

> **Important:** `pdflatex` must be installed inside the container (handled by the Dockerfile) or locally. The `%` and `$` characters in user data are automatically escaped to `\%` and `\$` to prevent LaTeX compilation errors.

---

## Testing

The project uses **pytest** with async support via `pytest-asyncio`. Tests are organized to mirror the `src/` structure:

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run a specific test file
uv run pytest tests/services/test_resume_service.py

# Run with coverage (if pytest-cov is installed)
uv run pytest --cov=src
```

**Test structure:**

```
tests/
├── conftest.py                         # Shared fixtures
├── controllers/
│   ├── test_auth_controller.py
│   └── test_resume_controller.py
├── generators/
│   ├── test_compile_pdf.py
│   ├── test_cv_pdf_generator.py
│   └── test_formatter.py
├── repositories/
│   ├── test_resume_repository.py
│   ├── test_skills_repository.py
│   └── test_users_repository.py
├── resume_generator/
│   └── test_resume_generator.py
├── services/
│   ├── test_auth_service.py
│   ├── test_resume_service.py
│   └── test_user_service.py
└── utils/
    ├── test_build_resume_reference.py
    ├── test_build_skill_entry.py
    ├── test_clean_json_output.py
    ├── test_generate_uuid.py
    ├── test_parse_resume_json.py
    └── test_security_utils.py
```

---

## Code References

- FastAPI app factory: [src/core/init_app.py](src/core/init_app.py)
- Application settings: [src/core/config.py](src/core/config.py)
- DynamoDB client: [src/core/db_client.py](src/core/db_client.py)
- API router registry: [src/core/router.py](src/core/router.py)
- Auth controller: [src/controllers/auth_controller.py](src/controllers/auth_controller.py)
- Resume controller: [src/controllers/resume_controller.py](src/controllers/resume_controller.py)
- Capybara controller: [src/controllers/capybara_resume_controller.py](src/controllers/capybara_resume_controller.py)
- CrewAI crew definition: [src/resume_generator/crew.py](src/resume_generator/crew.py)
- Agent definitions: [src/resume_generator/config/agents.yaml](src/resume_generator/config/agents.yaml)
- Task definitions: [src/resume_generator/config/tasks.yaml](src/resume_generator/config/tasks.yaml)
- Resume service (orchestrator): [src/services/resume_service.py](src/services/resume_service.py)
- Standard LaTeX template: [src/generators/resume_pdf/template.tex](src/generators/resume_pdf/template.tex)
- Capybara LaTeX template: [src/generators/resume_capybara/template.tex](src/generators/resume_capybara/template.tex)
- JWT security utilities: [src/utils/security.py](src/utils/security.py)
- JSON output cleaner: [src/utils/json_cleaner.py](src/utils/json_cleaner.py)
- Dockerfile: [Dockerfile](Dockerfile)
- Docker Compose (dev): [docker-compose.dev.yml](docker-compose.dev.yml)

---

## License

This project is licensed under the MIT License.

---

## Authors

<table align="center">
  <tr>
    <td align="center" style="padding:20px;">
      <a href="https://github.com/HugoAlejandro2002">
        <img src="https://avatars.githubusercontent.com/u/97768733?v=4"
             width="90"
             alt="HugoAlejandro"
             style="border-radius:50%" />
        <br />
        <sub><b>Hugo Alejandro Apaza</b></sub>
      </a>
      <br />
      <span style="font-size:13px; font-weight:600;">Author</span>
      <br />
      <span style="font-size:13px;">Backend & AI Developer · Cloud Engineer · Automation Specialist</span>
      <br /><br />
      <a href="https://www.linkedin.com/in/alejandro-apaza2002/">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
      </a>
      <a href="https://github.com/HugoAlejandro2002">
        <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
      </a>
    </td>
  </tr>
</table>