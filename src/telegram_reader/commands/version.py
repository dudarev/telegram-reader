import argparse

from .. import __version__


def cmd_version(args: argparse.Namespace) -> int:
    print(__version__)
    return 0


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    sp = subparsers.add_parser("version", help="Print version and exit")
    sp.set_defaults(func=cmd_version)