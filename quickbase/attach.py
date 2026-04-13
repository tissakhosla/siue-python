'''upload attachments to agreements table in quickbase'''

import base64
import logging
import glob
from pathlib import Path
from locale import getpreferredencoding

from . import args
from .const import AGR_TBL, ATT_TBL, QID, REPFIDS, FDIR
from .api import getReport, postAttachment

def extract(
        tid: str = AGR_TBL,
        qid: int = QID,
        repfids: tuple[str] = REPFIDS
        ) -> tuple[dict[str, str], list[str]]:
    '''return report data and pdf paths'''

    r = getReport(tid, qid)
    logging.info("< %-4s recs read", r.json()['metadata']['numRecords'])

    return {
        rec[repfids[0]]["value"]: rec[repfids[1]]["value"]
            for rec in r.json()["data"]
        }, sorted(glob.glob(f"{FDIR}/*.pdf"))

def transform(agrs: dict[str, str], pdfs: list[str]) -> list[dict]:
    '''create payload'''
    uplist = []

    for pdf in pdfs:
        for rid, name in agrs.items():
            fn = Path(pdf).name
            match = fn.split("_")[0]
            if match in name:
                with open(pdf, "rb") as f:
                    file_base64 = base64.b64encode(f.read()).decode(getpreferredencoding())

                title = " ".join(Path(fn).stem.split("_")[1:3]).strip()
                logging.info("> PDF: %-65s AGR: %-50s TIT: %-40s RID: %-3s", fn, name, title, rid)

                uplist.append(
                    {
                        "6": {
                            "value": title
                        },
                        "7": {"value": rid},
                        "8": {
                            "value": {
                                "fileName": fn,
                                "data": file_base64,
                            }
                        },
                    }
                )

    return uplist

def load(body: list[dict]):
    '''upload attachments to quickbase'''
    r = postAttachment(ATT_TBL, body)
    for rec in r.json()['data']:
        logging.info(
            "< PDF: %-65s AGR: %-50s TIT: %-40s",
            rec["8"]["value"]["versions"][0]["fileName"],
            rec["9"]["value"],
            rec["6"]["value"]
        )

    logging.info("< created rids: %s", r.json()['metadata']['createdRecordIds'])
    logging.info("# %-4s", r.json()['metadata']['totalNumberOfRecordsProcessed'])

def _main():
    logging.info("START DRY RUN" if args.dry_run else "START")

    agr_rids, pdf_paths = extract()
    body = transform(agr_rids, pdf_paths)

    if not args.dry_run:
        load(body)

    logging.info("END")
if __name__ == "__main__":
    _main()
