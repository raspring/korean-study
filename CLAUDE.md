# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
cd backend
cp .env.example .env   # fill in SECRET_KEY; optionally add Google OAuth creds
pip install -r requirements.txt
uvicorn main:app --reload
# → http://localhost:8000
```

The frontend is served by FastAPI at `/`. No separate frontend server needed.

## Architecture

**Frontend** — `index.html` (single file, no build step)
- Three study modes: Hangul chart, vocabulary flashcards, grammar reference, quiz
- All vocab/grammar data is in plain JS objects (`HANGUL`, `VOCAB`, `GRAMMAR`) at the top of the `<script>` block — extend these to add content
- Auth state: JWT stored in `localStorage`, loaded into `authToken` on startup
- `progressCache` (`"category:card_kr" → boolean`) mirrors DB state locally; updated optimistically on card mark
- On page load, `checkAuth()` validates the token, fetches progress, then calls `loadDeck()`
- Google OAuth redirect lands back at `/?token=<jwt>`, which `checkAuth()` picks up

**Backend** — `backend/` (FastAPI + SQLAlchemy)

| File | Purpose |
|------|---------|
| `main.py` | App entry point, mounts routers, serves `index.html` |
| `config.py` | Pydantic settings — reads from `.env` |
| `database.py` | SQLAlchemy engine + `get_db` dependency |
| `models.py` | `User`, `CardProgress`, `QuizScore` |
| `schemas.py` | Pydantic request/response models |
| `dependencies.py` | `get_current_user` — decodes Bearer JWT |
| `routers/auth.py` | `/api/auth/{register,login,me,google,google/callback}` |
| `routers/progress.py` | `GET/PUT /api/progress` — per-card known/unknown state |
| `routers/quiz.py` | `GET/POST /api/quiz/scores` |

**Database** — SQLite by default (`korean_study.db` created on first run). Switch to Postgres by setting `DATABASE_URL` in `.env`. Tables are created automatically via `Base.metadata.create_all()` in `main.py`.

**Auth flow**
- Email/password: `POST /api/auth/login` → JWT
- Google OAuth: browser → `/api/auth/google` → Google → `/api/auth/google/callback` → redirect to `/?token=<jwt>`
- All protected endpoints expect `Authorization: Bearer <token>`

## Google OAuth setup

1. Create a project at console.cloud.google.com
2. Enable the Google+ API / People API
3. Create OAuth 2.0 credentials (Web application)
4. Add `http://localhost:8000/api/auth/google/callback` as an authorized redirect URI
5. Copy client ID and secret into `.env`
