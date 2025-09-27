# Manual Testing Guide

Minimal scenarios to verify the CLI end-to-end. These tests require a working internet connection and valid Telegram API credentials.

## Prerequisites

- Create a config file at `~/.config/telegram-reader/config.yaml`:

```yaml
api_id: 123456
api_hash: "your_api_hash"
```

- Ensure the session directory is available: `~/.local/share/telegram-reader/`

## 1) Authenticate (first-time login)

Command:

```bash
tgr auth
```

Expected:
- Prompts for phone, then for the login code (and optional 2FA).
- Prints: `Authorized as: <id> @<username>`
- Creates a session file at `~/.local/share/telegram-reader/session.session`.

Notes:
- Subsequent runs should not prompt again.

## 2) List dialogs

Command:

```bash
tgr dialogs --limit 5
```

Expected:
- Prints up to 5 dialogs as a Markdown list, one per line, e.g.:

```
- 123456789 — Saved Messages
- -1001122334455 — My Channel
```

Notes:
- Output contains the dialog id and the human-readable title.

## 3) Read messages

Command (example with your own saved messages):

```bash
tgr messages --peer me --limit 10
```

Expected:
- Prints messages in Markdown blocks with second-level headers set to local timestamps (no seconds), e.g.:

```
## 2025-09-27 18:34

Hello world
```

- Empty/whitespace-only messages are omitted (e.g., sticker-only posts).
- A summary footer is printed on stderr, e.g.: `read 10 messages; next offset-id hint: 12345`

Optional checks:
- Use `--offset-id <n>` to paginate and confirm the footer hint works.
- Use `--reverse` to verify ordering changes.

Notes:
- Output is read-only: running these commands must not mark messages or dialogs as read in the Telegram app.
 - When using a numeric `--peer` (e.g., `1490343635` or `-1001234567890`), the peer must already appear in your dialogs list. Otherwise, use `@username` or a `t.me/...` link so it can be resolved.
