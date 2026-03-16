# cldpyprom01

Prototype of using AI to perform Read, Write, Update and Delete operations via REST API over SQLite DB.

## Overview

FastAPI-based REST API exposing full CRUD operations on a `Resource` table stored in a local SQLite database. The `Resource` entity models a person/contractor record including personal details, contact info, and allocation parameters.

A Streamlit chat interface powered by the Claude API allows interacting with the database using natural language — including uploading records from Excel files with conditional filters.

## Tech Stack

- **Python** 3.10+
- **FastAPI** — REST API framework
- **uvicorn** — ASGI server
- **SQLite** — local database (no setup required)
- **Pydantic** — request/response validation
- **Streamlit** — AI chat UI
- **Anthropic Claude API** — natural language to API call translation
- **pandas / openpyxl** — Excel file processing
- **Poetry** — dependency management

## Project Structure

```
cldpyprom01/
├── src/cldpyprom01/
│   ├── main.py        # FastAPI app entry point
│   ├── database.py    # SQLite connection and table init
│   ├── models.py      # Pydantic schemas (Create / Update / Response)
│   ├── router.py      # CRUD endpoint definitions
│   ├── ai_agent.py    # Claude API tool-use integration
│   └── chat.py        # Streamlit chat UI
├── .streamlit/
│   ├── secrets.toml.example   # Template for API key config
│   └── secrets.toml           # Your real keys — gitignored, never commit
├── tests/
├── pyproject.toml
└── CLAUDE.md
```

---

## Getting Started

### 1. Install dependencies

```bash
poetry install
```

### 2. Configure API key

Copy the example secrets file and add your Anthropic API key:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Get your key at: https://console.anthropic.com/settings/keys

---

## Running the Application

The app requires **two terminals running simultaneously**.

### Terminal 1 — REST API Server

```bash
cd c:\Users\mmsvo\OneDrive\Dokumenty\GitHub\cldpyprom01
poetry run uvicorn cldpyprom01.main:app --host 0.0.0.0 --port 8000 --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Keep this terminal open. The API server must be running before using the chat UI.

### Terminal 2 — AI Chat UI

Open a second terminal window, then:

```bash
cd c:\Users\mmsvo\OneDrive\Dokumenty\GitHub\cldpyprom01
poetry run streamlit run src/cldpyprom01/chat.py
```

Expected output:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

## Using the Chat UI

Open **http://localhost:8501** in your browser.

**Example instructions you can type:**
- `List all resources in the database`
- `Upload resources from the attached file, skip those with missing last name`
- `Delete resource with ID 5`
- `Upload only resources where email is filled in`

**To upload from Excel:**
1. Click **Browse files** in the left sidebar
2. Select your `.xlsx` or `.csv` file — a preview will appear
3. Type your instruction in the chat input
4. Claude will filter, upload, and report what was processed and what was skipped

---

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/resources/` | List all resources |
| `GET` | `/resources/{id}` | Get a single resource by ID |
| `POST` | `/resources/` | Create a new resource |
| `PUT` | `/resources/{id}` | Update an existing resource |
| `DELETE` | `/resources/{id}` | Delete a resource |

Interactive API docs (Swagger UI): http://localhost:8000/docs

---

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

---

## Notes

- The SQLite database file (`cldpyprom01.db`) is created automatically on first startup of the API server.
- Password fields from the original MariaDB schema are excluded from the API for security.
- `.streamlit/secrets.toml` is gitignored — never commit your real API key.
