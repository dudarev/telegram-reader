import argparse
import asyncio
import sys

from ..telethon_client import build_client, ensure_authorized


def cmd_auth(args: argparse.Namespace) -> int:
    bundle = build_client()
    client = bundle.client

    async def run() -> int:
        async with client:
            await ensure_authorized(bundle)
            me = await client.get_me()
            print(f"Authorized as: {me.id} @{getattr(me, 'username', None)}")
        return 0

    return asyncio.run(run())


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    sp = subparsers.add_parser("auth", help="Login and store session")
    sp.set_defaults(func=cmd_auth)