"""Parser for quickbase.attach."""

import argparse
from argparsers import add_dry_run_arg, build_parser


def _args() -> argparse.Namespace:
    parser = build_parser()
    add_dry_run_arg(parser)
    return parser.parse_args()


args = _args()
