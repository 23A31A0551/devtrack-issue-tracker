# DevTrack — Issue Tracking System (MVP)

A small working issue-tracking web app built with Python, Flask, and SQLite. Use it as a starter project, then extend it with Spring Boot/React, authentication, tests, and deployment for a stronger SDE portfolio.

## Features
- Create, view, edit, and delete issues
- Track project, assignee, priority, and status
- Search by title, project, or assignee
- Filter by status
- Dashboard counters
- SQLite persistence and sample data

## Run locally
Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

The SQLite database is created automatically on first run.

## GitHub
Create a repository named `devtrack-issue-tracker`, extract this ZIP, and upload its files.

## Next steps for a production-grade SDE portfolio
- Replace demo app with Java 17 + Spring Boot REST API and React/TypeScript frontend
- Add PostgreSQL, migrations, JWT authentication, and role-based access
- Add JUnit/Mockito tests, Docker, and GitHub Actions CI
- Add pagination, audit history, and API documentation

This is an MVP starter, not a production-secure service. Do not deploy with the demo secret key or debug mode enabled.
