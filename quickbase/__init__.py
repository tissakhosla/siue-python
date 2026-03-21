'''init'''
import logging
import argparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(module)s %(levelname)s %(funcName)-9s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def _args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="build payload only; do not post to Quickbase",
    )
    return p.parse_args()

args = _args()
