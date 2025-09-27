# telegram-reader

Minimal, read-only Telegram CLI tool designed for AI agents.

- Read messages from users/groups/channels
- List dialogs to discover peers
- Read-only: never sends messages
- XDG config in `~/.config/telegram-reader/config.yaml`
- Session stored in `~/.local/share/telegram-reader/`

## Install

We recommend using [uv](https://github.com/astral-sh/uv) for fast Python package management.

### Development Install

In your virtual env:

```bash
uv pip install -e .
```

To install testing dependencies (including pytest):

```bash
uv pip install -e .[test]
```

### Global Install

```bash
uv tool install .
```

For traditional pip-based installation, see the `pyproject.toml` for dependencies.

## Configure

Create `~/.config/telegram-reader/config.yaml`:

```yaml
api_id: 123456
api_hash: "your_api_hash"
# optional
default_limit: 10
```

Get `api_id` and `api_hash` from https://my.telegram.org

## Usage

- Initialize/login (prompts for phone, code, optional 2FA):

```bash
tgr auth
```

- Agent-focused help (compact guide for automation):

```bash
tgr agent
```

- List dialogs (prints a simple Markdown list):

```bash
tgr dialogs --limit 50
```

- Read messages from a peer (username, t.me link, or numeric id). Output is Markdown blocks with second-level headers set to local human-readable timestamps (YYYY-MM-DD HH:MM):

```bash
tgr messages --peer @durov --limit 10
```

Pagination options:

```bash
tgr messages --peer -1001234567890 --limit 50 --offset-id 12345
```

Outputs Markdown. Empty messages are omitted. A summary line with the next suggested `offset-id` is printed to stderr.

## Scope

- Read-only and minimal by design
- No sending/posting
- Telethon under the hood

## License

This project is licensed under the MIT License - see the LICENSE file for details.
