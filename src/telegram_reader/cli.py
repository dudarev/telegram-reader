from __future__ import annotations

import argparse
import sys
from typing import Optional

from . import __version__
from .commands import agent, auth, dialogs, messages, version


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="telegram-reader", description="Read-only Telegram CLI")
    # Standard version flag
    p.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="cmd")

    auth.add_subparser(sub)
    dialogs.add_subparser(sub)
    version.add_subparser(sub)
    agent.add_subparser(sub)
    messages.add_subparser(sub)

    return p


def main(argv: Optional[list[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
