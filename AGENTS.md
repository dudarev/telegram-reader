# Guidance for Repo-aware Agents

Scope: the entire repository.

- Keep the project minimal and read-only (no send/post features).
- Use standard library `argparse` for CLI (no Typer/Click).
- Use Telethon for Telegram API access.
- Config is XDG-compliant: `~/.config/telegram-reader/config.yaml` preferred; JSON accepted.
- Session path: `~/.local/share/telegram-reader/session.session`.
- Default message limit is 10; do not mark dialogs/messages as read.
- Outputs are Markdown by default for simplicity.
- Avoid adding unrelated dependencies.
- Tests: add lightweight unit tests only, no networked tests by default.
- Style: small, focused modules under `src/telegram_reader/`.

If you add files, keep them aligned with this structure:

- `src/telegram_reader/config.py` for config loading.
- `src/telegram_reader/cli.py` for CLI entry.
- `src/telegram_reader/telethon_client.py` for client/session/helpers.
- `src/telegram_reader/serialize.py` for output shaping.
- `tests/` for unit tests; network tests should be optional/skipped.

Versioning & changelog policy:
- When bumping the version, update it in both `pyproject.toml` and `src/telegram_reader/__init__.py` to keep them in sync.
- Every version change must be accompanied by an entry in `CHANGELOG.md` (Keep a Changelog format).

Process hygiene:
- For each implemented roadmap feature, bump the version, update the changelog, and suggest the user make an incremental commit when the feature is ready.

Secrets & git hygiene:
- Never commit real `config.yaml` / `config.json` with `api_id`/`api_hash`.
- Never commit Telethon session files (e.g., `*.session`, `*.session-journal`). Sessions live under `~/.local/share/telegram-reader/`.
- Local caches and coverage artifacts should be ignored (see `.gitignore`).
- Avoid printing secrets in test fixtures or logs; use stubs/mocks where needed.
