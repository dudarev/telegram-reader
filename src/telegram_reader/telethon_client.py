from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import re

from telethon import TelegramClient
from telethon.sessions import StringSession

from .config import AppConfig, Paths, ensure_dirs


@dataclass
class ClientBundle:
    client: TelegramClient
    paths: Paths
    config: AppConfig


def build_client(paths: Optional[Paths] = None, config: Optional[AppConfig] = None) -> ClientBundle:
    paths = paths or Paths()
    ensure_dirs(paths)
    if config is None:
        from .config import load_config
        config = load_config(paths)

    # Use a file session in data dir
    session_path = str(paths.session_path)
    client = TelegramClient(session_path, config.api_id, config.api_hash)
    return ClientBundle(client=client, paths=paths, config=config)


async def ensure_authorized(bundle: ClientBundle, phone: Optional[str] = None, password: Optional[str] = None) -> None:
    client = bundle.client
    if await client.is_user_authorized():
        return

    # Interactive login flow
    await client.connect()
    if not await client.is_user_authorized():
        if not phone:
            phone = input("Enter your phone number (in international format): ")
        sent = await client.send_code_request(phone)
        code = input("Enter the login code you received: ")
        try:
            await client.sign_in(phone=phone, code=code)
        except Exception as e:
            if 'SESSION_PASSWORD_NEEDED' in str(e).upper():
                if not password:
                    password = input("Two-step password: ")
                await client.sign_in(password=password)
            else:
                raise


def normalize_peer_id(raw: str) -> Optional[int]:
    """Parse a user/chat/channel ID from common textual inputs.

    Accepts:
    - plain digits like "1490343635"
    - negative ids like "-123456" (converted to positive)
    - channel-style "-1001234567890" (converted to positive)

    Returns the positive integer ID, or None if the input doesn't look numeric.
    """
    if raw is None:
        return None
    s = str(raw).strip()
    # strip common Telegram prefixes for chats/channels
    if s.startswith("-100"):
        s = s[4:]
    if s.startswith("-"):
        s = s[1:]
    if s.isdigit():
        try:
            return int(s)
        except ValueError:
            return None
    return None


async def resolve_peer(client: TelegramClient, peer: str):
    """Resolve a peer argument into an entity.

    Strategy:
    1) Try Telethon's native get_entity on the raw string (handles @user, t.me/... , me)
    2) If that fails and the input looks like a numeric id, scan dialogs to find a match
       by entity.id. This avoids needing an access_hash.
    """
    try:
        return await client.get_entity(peer)
    except Exception:
        pass

    target_id = normalize_peer_id(peer)
    if target_id is None:
        # Re-raise a consistent error to the caller
        raise ValueError(f"Cannot resolve peer: {peer!r}")

    # Fallback: search through known dialogs for matching entity id
    async for d in client.iter_dialogs(limit=None):
        ent = getattr(d, "entity", None)
        if getattr(ent, "id", None) == target_id:
            return ent

    raise ValueError(
        "Cannot find any entity by numeric id. "
        "Ensure the user/chat/channel is in your dialogs or use @username/t.me link."
    )
