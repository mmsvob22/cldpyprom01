# cldpyprom01

## Project Overview
<"Prototype of using AI to perform Read, Write, Update and Delete operations via REST API over SQL lite DB "->

## Tech Stack
- Language: Python 3.10+
- Package manager: Poetry
- Structure: src layout

## Commands
```bash
# Run REST API server (terminal 1)
poetry run uvicorn cldpyprom01.main:app --host 0.0.0.0 --port 8000 --reload

# Run AI Chat UI (terminal 2)
poetry run streamlit run src/cldpyprom01/chat.py

# Install dependencies
poetry install

# Add a dependency
poetry add <package>
```

## Project Structure
```
cldpyprom01/
├── src/cldpyprom01/
│   ├── __init__.py
│   ├── main.py        # FastAPI app entry point
│   ├── database.py    # SQLite connection and table init
│   ├── models.py      # Pydantic schemas
│   ├── router.py      # CRUD endpoints
│   ├── ai_agent.py    # Claude API tool-use integration
│   └── chat.py        # Streamlit chat UI
├── .streamlit/
│   └── secrets.toml   # API keys (gitignored — copy from secrets.toml.example)
├── tests/
├── pyproject.toml
└── CLAUDE.md
```

## Secrets Setup
Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

## Code Style
- snake_case for variables and functions
- PascalCase for classes
- f-strings preferred over .format()
- Keep secrets out of source — use .env or secrets.toml (gitignored)

## Known Behaviours
- If the Streamlit chat returns an API error, click "Clear conversation" in the sidebar before retrying
- The REST API server (port 8000) must be running before starting the chat UI
- Streamlit must be run via `poetry run` so the package is on the Python path

## What NOT to Do
- Don't commit .env or secrets.toml
- Don't hardcode credentials
