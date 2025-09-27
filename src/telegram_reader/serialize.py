from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from telethon.tl.types import Message


def _to_local_human(dt: datetime) -> str:
    """Return a human-readable local timestamp without seconds.

    - If `dt` is timezone-aware, convert to local time.
    - If `dt` is naive, assume UTC and convert to local time.
    - Format: YYYY-MM-DD HH:MM
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    local = dt.astimezone()
    return local.strftime("%Y-%m-%d %H:%M")


def message_to_markdown_block(m: Message) -> Optional[str]:
    """Format a single Telethon Message as a Markdown block.

    - Header level 2 with local human-readable timestamp
    - Body is the message text as-is
    - Returns None if message text is empty/whitespace
    - Media is omitted
    """
    text = getattr(m, "message", None) or ""
    if text.strip() == "":
        return None

    date = getattr(m, "date", None)
    if isinstance(date, datetime):
        ts = _to_local_human(date)
    else:
        ts = ""  # Fallback if no date; still render text

    header = f"## {ts}" if ts else "## "
    return f"{header}\n\n{text}"


def write_markdown_blocks(blocks: Iterable[str]) -> None:
    """Print pre-formatted markdown blocks separated by a blank line."""
    first = True
    for block in blocks:
        if block is None:
            continue
        if not first:
            print()
        print(block)
        first = False


def dialog_to_markdown_line(d: Dict[str, Any]) -> str:
    """Render a dialog entry into a single markdown list line.

    Expected fields in d: id, title. Other fields are ignored.
    """
    did = d.get("id", "?")
    title = d.get("title", "") or "(no title)"
    return f"- {did} — {title}"


def write_dialogs_markdown(dialogs: Iterable[Dict[str, Any]]) -> None:
    lines = (dialog_to_markdown_line(d) for d in dialogs)
    for line in lines:
        print(line)
