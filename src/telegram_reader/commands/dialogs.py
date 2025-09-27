import argparse
import asyncio
import sys

from ..telethon_client import build_client, ensure_authorized
from ..serialize import write_dialogs_markdown


def cmd_dialogs(args: argparse.Namespace) -> int:
    bundle = build_client()
    client = bundle.client

    async def run() -> int:
        async with client:
            await ensure_authorized(bundle)
            items = []
            async for d in client.iter_dialogs(limit=args.limit):
                items.append({
                    "id": getattr(d.entity, 'id', None),
                    "title": d.name,
                    "is_channel": getattr(d.entity, '__class__', type(None)).__name__.endswith('Channel'),
                    "is_user": getattr(d.entity, '__class__', type(None)).__name__.endswith('User'),
                    "is_chat": getattr(d.entity, '__class__', type(None)).__name__.endswith('Chat'),
                    "username": getattr(d.entity, 'username', None),
                })
            write_dialogs_markdown(items)
        return 0

    return asyncio.run(run())


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    sp = subparsers.add_parser("dialogs", help="List dialogs")
    sp.add_argument("--limit", type=int, default=50)
    sp.set_defaults(func=cmd_dialogs)