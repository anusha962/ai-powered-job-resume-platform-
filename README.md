# AI Resume & Job Platform

Full-stack app: **React** frontend + **Django REST Framework** backend, with
an NLP/LLM-powered RAG pipeline for resume-to-job matching. Deploys to
**Render** as two services (API + static frontend) plus a managed Postgres
database.

## What it does

- **Resume upload & parsing** — extracts text from PDF/DOCX resumes.
- **Skill extraction** — keyword/phrase matching over a tech skill taxonomy
  (`core/utils/skill_extraction.py`). Lightweight by design so it deploys
  cleanly on Render's free tier, no heavy model downloads.
- **ATS-style scoring** — heuristic score (0–100) covering resume sections,
  skill breadth, length, and quantified achievements
  (`core/utils/ats_scoring.py`).
- **RAG matching pipeline** (`core/utils/rag_matcher.py`):
  - *Retrieval*: TF-IDF + cosine similarity ranks job postings against a
    resume, and skills are diffed to find gaps.
  - *Generation*: the retrieved job description + missing skills are passed
    to an LLM (Claude, via the Anthropic API) to generate tailored
    interview questions grounded in that context.
- **Job recommendation engine** — the retrieval step above, exposed as
  `GET /api/resumes/{id}/recommendations/`.
- **Application tracker** — save jobs and move them through
  saved → applied → interview → offer/rejected.

## Project structure

```
job-platform/
├── backend/            Django + DRF API
│   ├── jobplatform/     settings, urls, wsgi
│   └── core/             models, serializers, views, utils/
├── frontend/            React (Vite) app
│   └── src/
│       ├── components/  ResumeUpload, ScoreCard, JobMatches, JobBoard, ApplicationTracker
│       └── api.js       fetch wrapper for the DRF API
└── render.yaml          Render Blueprint (provisions API + frontend + DB)
```

## Local development

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # edit as needed; SQLite is used if DATABASE_URL is unset
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

API is now at `http://localhost:8000/api/`.

To get real LLM-generated interview questions (instead of the templated
fallback), set `ANTHROPIC_API_KEY` in `backend/.env`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # VITE_API_URL=http://localhost:8000/api
npm run dev
```

App is now at `http://localhost:5173/`.

## Deploying to Render

1. Push this repo to GitHub.
2. In the Render dashboard: **New → Blueprint**, point it at the repo.
   Render reads `render.yaml` and provisions:
   - `job-platform-db` — a free Postgres instance
   - `job-platform-api` — the Django API (gunicorn, migrations run on build)
   - `job-platform-frontend` — the React app as a static site
3. In the `job-platform-api` service settings, add your `ANTHROPIC_API_KEY`
   as an environment variable (marked `sync: false` in the blueprint so it
   isn't committed to git).
4. Once both services are live, double check `FRONTEND_URL` on the API
   service and `VITE_API_URL` on the frontend service match the actual
   `.onrender.com` URLs Render assigned (the blueprint guesses the default
   naming, but confirm after first deploy — Render appends a random suffix
   if a name is taken).
5. Redeploy the frontend if you had to change `VITE_API_URL`, since Vite
   bakes env vars in at build time.

**Note on file storage:** Render's free-tier filesystem is ephemeral, so
uploaded resume files won't survive a redeploy. For production use, swap
`Resume.file` to use S3-backed storage (e.g. `django-storages`) — the
extracted text and skills are already persisted in Postgres either way.

## API reference

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/resumes/` | Upload a resume (`file` field); returns extracted text, skills, ATS score |
| GET | `/api/resumes/{id}/recommendations/` | Ranked job matches (retrieval step) |
| POST | `/api/resumes/{id}/match/` | Full match + LLM interview questions for one job (`{"job_id": n}`) |
| GET/POST | `/api/jobs/` | List / create job postings |
| GET | `/api/matches/?resume={id}` | Saved matches for a resume |
| GET/POST/PATCH | `/api/applications/` | Application tracker CRUD |
