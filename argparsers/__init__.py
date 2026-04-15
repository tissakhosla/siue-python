"""Shared parser helpers for runnable modules."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Create a standard parser instance."""
    return argparse.ArgumentParser()


def add_dry_run_arg(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Attach the common dry-run flag."""
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="build payload only; do not post to Quickbase",
    )
    return parser
