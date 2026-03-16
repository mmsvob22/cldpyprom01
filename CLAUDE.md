# cldpyprom01

## Project Overview
<"Prototype of using AI to perform Read, Write, Update and Delete operations via REST API over SQL lite DB "->

## Tech Stack
- Language: Python 3.10+
- Package manager: Poetry
- Structure: src layout

## Commands
```bash
# Run API server
poetry run uvicorn cldpyprom01.main:app --host 0.0.0.0 --port 8000 --reload

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
│   └── main.py       # Entry point
├── tests/
├── pyproject.toml
└── CLAUDE.md
```

## Code Style
- snake_case for variables and functions
- PascalCase for classes
- f-strings preferred over .format()
- Keep secrets out of source — use .env or secrets.toml (gitignored)

## What NOT to Do
- Don't commit .env or secrets.toml
- Don't hardcode credentials
