'''constants'''
import os

WD = os.getcwd()
FDIR = "/home/ubuntu/projects/finity/siue/attachments"
# FDIR = f"{WD}/data/attachments/"

# agreements tbl, attachments tbl
# report to get 'agr rid', 'rel counterparty name'
# fid for rel agr in attachment tbl
# fids for posting attachment (title, file, rel agr name)
AGR_TBL, ATT_TBL = "bvt33a9pv", "bvv3u52mn"
QID, REPFIDS = 7, ("3", "11")

ATTACH_TITLE, ATTACH_REL_AGR, ATTACH_FILE, REL_AGR_NAME, ATTACH_TYPE \
      = 6, 7, 8, 9, 10

ATTACH_FIDS = RET_FIDS = [ATTACH_TITLE, ATTACH_FILE, REL_AGR_NAME]

REALM = os.getenv("SIUE_QB_REALM")
AUTH = os.getenv("SIUE_QB_UTOKEN")

assert REALM is not None, "REALM env var not set"
assert AUTH is not None, "AUTH env var not set"

HDR = {
    "Content-Type": "application/json",
    "QB-Realm-Hostname": REALM,
    "User-Agent": "tk-python-upload-attachments",
    "Authorization": f"QB-USER-TOKEN {AUTH}",
}
