"""Parser for quickbase.single."""

import argparse
from argparsers import add_dry_run_arg, build_parser


def _args() -> argparse.Namespace:
    parser = build_parser()
    add_dry_run_arg(parser)
    parser.add_argument(
        "agreement_rid",
        help="agreement record id",
    )
    parser.add_argument(
        "attachment_type",
        help="attachment type",
    )
    parser.add_argument(
        "attachment_directory",
        help="path to pdfs to upload as attachments",
    )
    return parser.parse_args()


args = _args()
