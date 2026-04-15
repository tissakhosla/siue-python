'''upload attachments to attachments table in agreement tracker w rel agr param'''

import base64
import logging as log
from glob import glob
from pathlib import Path
from locale import getpreferredencoding
from argparsers.single import args
from .const import ATTACH_TITLE, ATTACH_REL_AGR, ATTACH_FILE, ATTACH_TYPE
from .api import postAttachment
from .const import ATT_TBL

def extract(dirpath: str) -> list[str]:
    '''return attachments'''
    return sorted(
        glob(f"{dirpath}/*.pdf") +
        glob(f"{dirpath}/*.PDF") +
        glob(f"{dirpath}/*.docx")
    )

def transform(pdfs: list[str]) -> list[dict]:
    '''create payload'''
    return [
        {
            str(ATTACH_TITLE): {
                "value": Path(pdf).stem
            },
            str(ATTACH_REL_AGR): {
                "value": args.agreement_rid
            },
            str(ATTACH_FILE): {
                "value": {
                    "fileName": Path(pdf).name,
                    "data": base64.b64encode(open(pdf, "rb").read()).decode(getpreferredencoding()),
                }
            },
            str(ATTACH_TYPE): {
                "value": args.attachment_type
            },
        }
        for pdf in pdfs
    ]

def _main():
    '''main'''
    for dirpath in [args.attachment_directory]:
        log.info("< dir: %s", dirpath)
        pdfs = extract(dirpath)
        for pdf in pdfs:
            log.info("> %s", pdf)
        payload = transform(pdfs)
        if not args.dry_run:
            res = postAttachment(ATT_TBL, payload)
            log.info("> response: %s", res.status_code)
            if res.status_code != 200:
                log.error("> response content: %s", res.content)
            for rec in res.json()['data']:
                log.info(
                    "< PDF: %-65s AGR: %-50s TIT: %-40s",
                    rec["8"]["value"]["versions"][0]["fileName"],
                    rec["9"]["value"],
                    rec["6"]["value"]
                )

            log.info("< created rids: %s", res.json()['metadata']['createdRecordIds'])
            log.info("# %-4s", res.json()['metadata']['totalNumberOfRecordsProcessed'])

if __name__ == "__main__":
    _main()
