# cldpyprom01

Prototype of using AI to perform Read, Write, Update and Delete operations via REST API over SQLite DB.

## Overview

FastAPI-based REST API exposing full CRUD operations on a `Resource` table stored in a local SQLite database. The `Resource` entity models a person/contractor record including personal details, contact info, and allocation parameters.

## Tech Stack

- **Python** 3.10+
- **FastAPI** — REST API framework
- **uvicorn** — ASGI server
- **SQLite** — local database (no setup required)
- **Pydantic** — request/response validation
- **Poetry** — dependency management

## Project Structure

```
cldpyprom01/
├── src/cldpyprom01/
│   ├── main.py        # FastAPI app entry point
│   ├── database.py    # SQLite connection and table init
│   ├── models.py      # Pydantic schemas (Create / Update / Response)
│   └── router.py      # CRUD endpoint definitions
├── tests/
├── pyproject.toml
└── CLAUDE.md
```

## Getting Started

### Install dependencies

```bash
poetry install
```

### Run the server

```bash
poetry run uvicorn cldpyprom01.main:app --host 0.0.0.0 --port 8000 --reload
```

### Open the API docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/resources/` | List all resources |
| `GET` | `/resources/{id}` | Get a single resource by ID |
| `POST` | `/resources/` | Create a new resource |
| `PUT` | `/resources/{id}` | Update an existing resource |
| `DELETE` | `/resources/{id}` | Delete a resource |

## Resource Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `first_name` | string | Yes | First name |
| `last_name` | string | Yes | Last name |
| `middle_name` | string | No | Middle name |
| `company` | string | No | Company name |
| `alloc_work_hours` | int | No | Standard working hours |
| `alloc_max_hours` | int | No | Maximum working hours |
| `alloc_night_work` | bool | No | Night work allowed |
| `alloc_overtime` | bool | No | Overtime allowed |
| `alloc_weekend` | bool | No | Weekend work allowed |
| `contact_email` | string | No | Email address |
| `contact_mobile_phone` | string | No | Mobile phone |
| `contact_city` | string | No | City |
| `contact_country` | string | No | Country |
| `registration_status` | string | No | Registration status |
| `created_by` | string | Yes | Creator identifier |

## Notes

- The SQLite database file (`cldpyprom01.db`) is created automatically on first startup.
- Password fields from the original MariaDB schema are excluded from the API for security.
