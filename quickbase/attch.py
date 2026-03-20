'''upload attachments to agreements table in quickbase'''

import base64
from pathlib import Path
import json
import logging
import glob

from .api import getReport, postAttachment

WD = "/home/ubuntu/projects/finity/siue/siue-python"
FDIR = f"{WD}/data/attachments/"
TID = "bvt33a9pv" # agreements table
QID = 7 # report to get agreement rid, rel counterparty name

REPFIDS = ["3", "11"] # fields from report: rid and related counterparty name 
REL_AGR = "7" # field id for related agreement in attachment table

def extract(
        tid: str = TID,
        qid: int = QID,
        repfids: list[str] = REPFIDS
        ) -> tuple[dict[str, str], list[str]]:
    '''get report data and pdf paths'''
    r = getReport(tid, qid)
    logging.info(r.status_code)

    return {
        rec[repfids[0]]["value"]: rec[repfids[1]]["value"] 
            for rec in r.json()["data"]
        }, sorted(glob.glob(f"{FDIR}/*.pdf"))

def transform(agrs, pdfs):
    uplist = list()
    for pdf in pdfs:
        for rid, name in agrs.items():
            fn = Path(pdf).name
            match = fn.split("_")[0]
            if match in name:
                with open(pdf, "rb") as f:
                    file_base64 = base64.b64encode(f.read()).decode("utf-8")
                logging.info("PDF: %s AGR: %s RID: %s", fn, name, rid)
                uplist.append(
                    {
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
    r = postAttachment(TID, body)
    logging.info(r.status_code)
    logging.info(r.text)

def _main():

    agr_rids, pdf_paths = extract()
    body = transform(agr_rids, pdf_paths)
    load(body)

if __name__ == "__main__":
    _main()
