import argparse
import asyncio
import sys
from typing import List

from ..telethon_client import build_client, ensure_authorized, resolve_peer
from ..serialize import message_to_markdown_block, write_markdown_blocks


def _print_err(msg: str) -> None:
    print(msg, file=sys.stderr)


def cmd_messages(args: argparse.Namespace) -> int:
    bundle = build_client()
    client = bundle.client

    async def run() -> int:
        async with client:
            await ensure_authorized(bundle)
            if not args.peer:
                _print_err("--peer is required")
                return 2
            try:
                entity = await resolve_peer(client, args.peer)
            except ValueError as e:
                _print_err(str(e))
                return 2

            count = 0
            last_id = None
            blocks: List[str] = []
            raw_messages = []
            async for m in client.iter_messages(
                entity, limit=args.limit, offset_id=args.offset_id, reverse=False
            ):
                raw_messages.append(m)
                last_id = m.id

            # Reverse to output in chronological order (oldest first)
            for m in reversed(raw_messages):
                count += 1
                block = message_to_markdown_block(m)
                if block:
                    blocks.append(block)
            write_markdown_blocks(blocks)
            # Separator to visually distinguish summary from message output when streams are merged
            _print_err("\n\n---")
            _print_err(f"read {count} messages; next offset-id hint: {last_id}")
        return 0

    return asyncio.run(run())


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    sp = subparsers.add_parser("messages", help="Read messages from a peer")
    sp.add_argument("--peer", required=True, help="@username, t.me/..., or numeric id")
    sp.add_argument("--limit", type=int, default=10)
    sp.add_argument("--offset-id", type=int, default=0)
    sp.set_defaults(func=cmd_messages)