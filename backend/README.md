# BAHO Market Backend

Production-oriented Django backend foundation for BAHO Market e-commerce.

## Stack

- Python 3.12
- Django 5 + DRF
- PostgreSQL
- Redis
- Celery
- Gunicorn
- Nginx
- Docker Compose

## Quick Start (Docker)

1. Copy env:

```bash
cp .env.example .env
```

2. Start services:

```bash
docker compose up --build
```

3. API endpoints:

- Health: `http://localhost:8000/api/v1/core/health/`
- Swagger: `http://localhost:8000/api/docs/swagger/`
- ReDoc: `http://localhost:8000/api/docs/redoc/`
- Admin: `http://localhost:8000/admin/`

## Local Development (without Docker)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Phase 1 Scope Completed

- Split settings (`base`, `local`, `production`)
- PostgreSQL + Redis config
- Celery bootstrap and worker/beat services
- JWT/DRF baseline, throttling, filtering, pagination
- OpenAPI (drf-spectacular)
- Dockerfile + Compose + Nginx
- Healthcheck API and initial test
