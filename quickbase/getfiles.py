'''Download files from Quickbase Attachment Table'''

import logging as log
from pathlib import Path

from cgi import parse_header
from urllib.parse import unquote

from .api import getReport, getFile
from .const import ATT_TBL, ATT_QID, ATTACH_FILE


def extract() -> list[dict]:
    """Run the report to get the attachment paths."""
    r = getReport(ATT_TBL, ATT_QID)
    log.info("< %-4s recs read", r.json()['metadata']['numRecords'])
    return [
        {
            "name": rec[str(ATTACH_FILE)]["value"]["versions"][0]["fileName"],
            "version": rec[str(ATTACH_FILE)]["value"]["versions"][0]["versionNumber"],
            "rid": rec["3"]["value"]
        }
        for rec in r.json()["data"]
    ]

def transform(rec: dict) -> tuple[bytes, str]:
    """Get the b64 file data for each attachment."""

    f = getFile(ATT_TBL, str(rec["rid"]), str(ATTACH_FILE), str(rec["version"]))
    cd = f.headers.get("Content-Disposition", "")
    _, params = parse_header(cd)

    if "filename*" in params:
        filename = unquote(params["filename*"].split("''", 1)[-1])
    else:
        filename = params.get("filename")

    attachment = f.content

    log.info("< %-60s %8.2f KB", filename, len(attachment) / 1024)
    return attachment, filename

def load(c: bytes, fn: str):
    """Save the files to disk."""
    out_dir = Path("data/attachments")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / fn
    with open(out_path, "wb") as f:
        f.write(c)
    log.info("> %s", out_path)

def _main():
    log.info("START")

    dat = extract()
    for rec in dat:
        content, fn = transform(rec)
        load(content, fn)
    log.info("END")

if __name__ == "__main__":
    _main()
