"""Helpers for fulfillment attachment RID mapping."""
import csv
import base64
import logging as log
from pathlib import Path
from locale import getpreferredencoding

from argparsers.attach import args
from .const import ATTACH_REL_FUL, ATTACH_FILE,\
                   ATT_TBL, ATTACH_TYPE
from .api import postFulfillment

def extract() -> list[tuple[str, str]]:
    """Read the fulfill RID CSV and return (path, record id) pairs."""

    csvfile = Path("/home/ubuntu/projects/finity/siue/sandbox/fulfill_rid.csv")
    rows: list[tuple[str, str]] = []

    with csvfile.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            path = (row.get("PATH") or "").strip()
            record_id = (row.get("REL") or "").strip()
            assert Path(path).is_file(), f"File not found: {path}"

            assert path and record_id, f"Invalid row: {row}"
            rows.append((path, record_id))
    return rows

def transform(plist: list[tuple[str, str]]) -> list[dict]:
    """Transform pairs into a list of payloads for Quickbase."""
    uplist = []
    for p, rid in plist:
        with open(p, "rb") as f:
            file_base64 = base64.b64encode(f.read()).decode(getpreferredencoding())

        uplist.append({
            str(ATTACH_REL_FUL): {"value": rid},
            str(ATTACH_FILE): {
                "value": {
                    "fileName": Path(p).name,
                    "data": file_base64
                }
            },
            str(ATTACH_TYPE): {"value": "Deposit"}
        })

    return uplist

def load(body: list[dict]):
    """Upload the attachments to Quickbase."""
    r = postFulfillment(ATT_TBL, body)
    for rec in r.json()['data']:
        log.info(
            "< PDF: %-65s AGR: %-50s",
            rec["8"]["value"]["versions"][0]["fileName"],
            rec["12"]["value"],
        )

    log.info("< created rids: %s", r.json()['metadata']['createdRecordIds'])
    log.info("# %-4s", r.json()['metadata']['totalNumberOfRecordsProcessed'])

def _main():
    log.info("START")
    fmap = extract()
    log.info("# %d extracted", len(fmap))
    payload = transform(fmap)
    log.info("# %d transformed", len(payload))
    if not args.dry_run:
        assert payload, "No payloads to upload"
        assert len(payload) == len(fmap), "Payload and fmap lengths do not match"

        load(payload)
    log.info("END")

if __name__ == "__main__":
    _main()
