from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional, Tuple

from telethon.tl.types import Message, PeerUser, PeerChat, PeerChannel


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

    # Sender attribution
    author = _format_sender(m)

    header = f"## {ts}" if ts else "## "
    if author:
        header = f"{header} — {author}"

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


def _sender_kind_and_id(m: Message) -> Tuple[Optional[str], Optional[int]]:
    """Infer sender kind and numeric id from a message.

    Returns (kind, id) where kind is one of 'user', 'chat', 'channel', or None.
    """
    from_id = getattr(m, "from_id", None)
    if isinstance(from_id, PeerUser):
        return ("user", int(from_id.user_id))
    if isinstance(from_id, PeerChat):
        return ("chat", int(from_id.chat_id))
    if isinstance(from_id, PeerChannel):
        return ("channel", int(from_id.channel_id))

    # Fallbacks: try sender_id if present (assume user)
    sid = getattr(m, "sender_id", None)
    if isinstance(sid, int):
        return ("user", int(sid))
    return (None, None)


def _format_sender(m: Message) -> str:
    """Produce a compact, privacy-conscious sender label for a message.

    Rules:
    - Outgoing messages: 'ME'.
    - Prefer '@username' when available.
    - Otherwise use display name if present.
    - Add an id suffix like '[channel 12345]' when the kind is not 'user',
      or when the user has no username (to help disambiguate common names).
    - For channel posts with a signed 'post_author', append it: '… — Author'.
    """
    # Outgoing
    if bool(getattr(m, "out", False)):
        return "ME"

    kind, ident = _sender_kind_and_id(m)

    # Try to use sender entity when available (may not always be cached)
    sender = getattr(m, "sender", None)
    username = None
    name = None
    if sender is not None:
        username = getattr(sender, "username", None)
        first = getattr(sender, "first_name", None)
        last = getattr(sender, "last_name", None)
        name = " ".join(p for p in [first, last] if p)
        name = name or None

    # Build base label
    base = None
    if username:
        base = f"@{username}"
        if name and name != username:
            base = f"{name} ({base})"
    elif name:
        base = name
    elif kind and ident is not None:
        base = f"{kind} {ident}"
    else:
        base = "unknown"

    # Decide on id suffix
    suffix = ""
    if kind in {"chat", "channel"} and ident is not None:
        suffix = f" [{kind} {ident}]"
    elif kind == "user" and not username and ident is not None:
        suffix = f" [user {ident}]"

    # Channel post author signature
    post_author = getattr(m, "post_author", None)
    if post_author and kind == "channel":
        return f"{base}{suffix} — {post_author}"

    return f"{base}{suffix}"
