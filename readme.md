# Gig Worker Platform (Backend)

A Django REST Framework backend for a gig worker platform where users can register, become workers, upload verification documents, and manage profiles using JWT authentication (For now).

---

## Features

### Authentication

- User registration
- JWT login and refresh tokens (SimpleJWT)

### User Module

- View logged-in user profile
- Delete own account
- User profile created automatically after registration

### Worker Module

- Become a worker (creates WorkerProfile + updates user_type)
- Upload worker documents (Citizenship, Driver License, etc.)
- Worker verification and approval can be managed using Django Admin

---

## Tech Stack

- Python 3.12
- Django 5
- Django REST Framework
- PostgreSQL (or SQLite for development)
- SimpleJWT (JWT Authentication)
- Pillow (for images)

---

## API Docs

After running the server, use these documentation URLs:

- OpenAPI Schema (JSON): `/api/schema/`
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

Swagger UI supports Bearer JWT auth directly. Use the access token from `/api/token/`.

---

## API Reference (Current)

### Auth

- `POST /accounts/register/`
- `POST /api/token/`
- `POST /api/token/refresh/`

### Accounts

- `GET /accounts/me/`
- `GET, PATCH /accounts/profile/`
- `POST /accounts/become-worker/`
- `GET, PATCH /accounts/worker/profile/`
- `GET /accounts/worker/documents/`
- `POST /accounts/worker/documents/upload/`
- `PATCH /accounts/worker/availability/`

### Admin Verification

- `GET /accounts/admin/workers/pending/`
- `POST /accounts/admin/workers/{worker_id}/verify/`
- `POST /accounts/admin/documents/{document_id}/verify/`

### Services

- `GET /services/categories/`
- `GET /services/recommended-workers/?service_category=<name>&radius=<km>`
- `GET, POST /services/requests/`
- `GET /services/worker/inbox/`
- `POST /services/worker/inbox/{broadcast_id}/action/`
- `POST /services/requests/{request_id}/worker-status/`

### Ratings & Ranking

- `GET, POST /ratings/reviews/`
- `GET /ratings/reviews/?worker_id={worker_user_uuid}`
- `GET /ratings/sentiments/`
- `GET /ratings/leaderboard/`
