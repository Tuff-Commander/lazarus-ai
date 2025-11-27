# Lazarus AI Architecture & Standards

## Project Purpose
Lazarus AI is a tool that automatically resurrects abandoned GitHub projects. It scans for dead dependencies, security vulnerabilities, and deprecated code, then fixes them automatically.

## Tech Stack
- **Core Logic:** Python 3.10+
- **CLI Interface:** Click (Python library)
- **Target Ecosystem:** Node.js/JavaScript repositories
- **Testing:** Pytest

## Core Modules (src/)
- `scanner.py`: Analyzes GitHub repos, parses package.json, checks vulnerabilities.
- `dependency_manager.py`: Handles npm/yarn updates and semantic versioning logic.
- `security_patcher.py`: Cross-references vulnerabilities and applies patches.
- `code_modernizer.py`: Uses AST parsing to update syntax (e.g., var -> const).
- `cli.py`: The entry point for the command line interface.

## Coding Standards (STRICT)
1. **Safety First:** All file operations must be reversible.
2. **Type Hinting:** All Python functions must use strict type hints.
3. **Error Handling:** Use `try/except` blocks with specific error messages (not just `pass`).
4. **Async/Await:** Use `asyncio` for network requests (GitHub API, NPM Registry).
5. **Rich Output:** Use the `rich` library for all terminal outputs (color, emojis, progress bars).