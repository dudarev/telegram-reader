import argparse

from .. import __version__


def cmd_agent(args: argparse.Namespace) -> int:
    """Print an agent-focused, concise usage guide."""
    guide = f"""
telegram-reader — agent guide

Purpose
- Minimal, read-only Telegram CLI. No sending or marking as read.

Config & Session
- Config (YAML preferred): ~/.config/telegram-reader/config.yaml
- JSON also accepted: ~/.config/telegram-reader/config.json
- Session path: ~/.local/share/telegram-reader/session.session
- Required keys in config: api_id (int), api_hash (str)

Auth
- Login and persist session:
  tgr auth
- Output: "Authorized as: <id> @<username>"

Dialogs
- List recent dialogs (id and title):
  tgr dialogs --limit 20
- Output: Markdown list lines, e.g. "- 123456789 — Saved Messages"

Messages
- Read messages from a peer:
  tgr messages --peer @username --limit 10
  tgr messages --peer t.me/some_channel --limit 10
  tgr messages --peer me --limit 10
  tgr messages --peer -1001234567890 --limit 50 --offset-id 12345
- Output: Markdown blocks per message with "## YYYY-MM-DD HH:MM" headers; empty messages omitted.
- Footer on stderr: "read N messages; next offset-id hint: <last_id>"
- Notes on --peer:
  - @username and t.me/... resolve directly.
  - Numeric ids (e.g., 1490343635 or -100...) must exist in your dialogs.

Pagination & Order
- Use --offset-id <n> as a starting point.
- Add --reverse to read forward (newer first).

Defaults & Behavior
- Default message limit: 10.
- Read-only: commands do not mark dialogs/messages as read.

Exit codes
- 0 on success; 2 on invalid input (e.g., bad --peer); 130 on Ctrl-C.
""".strip()
    print(guide)
    return 0


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    sp = subparsers.add_parser("agent", help="Print agent-focused usage guide")
    sp.set_defaults(func=cmd_agent)