# cldpyprom01

## Project Overview
<!-- Describe what this project does -->

## Tech Stack
- Language: Python 3.10+
- Package manager: Poetry
- Structure: src layout

## Commands
```bash
# Run main script
poetry run python src/cldpyprom01/main.py

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
