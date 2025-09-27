# Roadmap

Lightweight plan for future improvements. Keep scope minimal and read-only.

## CLI & Config
- Global defaults via config for output format and limits.
- Non-interactive auth support via environment variables (opt-in), without persisting secrets.

## Code Quality
- Add formatting and linting (e.g., Ruff for linting and formatting) with pre-commit hooks.
- Type checking with mypy (strict where reasonable) and CI gate.

## Features (Read-only)
- Export dialogs/messages to files (markdown) without marking read.
- Optional date/time filters for messages.
- Message text-only vs full metadata toggle (still read-only, no media downloading by default).

## Docs
- Expand examples for pagination and numeric peer resolution.
- Security note on keeping `api_hash`, sessions, and configs out of VCS.

Notes
- Avoid adding non-essential dependencies; prefer stdlib and Telethon.
- No send/post features; do not mark dialogs/messages as read.
