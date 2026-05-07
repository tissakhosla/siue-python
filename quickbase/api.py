'''api calls to quickbase'''

import logging as log
import requests
from .const import HDR, ATTACH_RET_FIDS, FULFILL_RET_FIDS


def _get(url: str, headers: dict | None = None, timeout: int = 30, **kwargs):
    return requests.get(
        url=url,
        headers=headers if headers is not None else HDR,
        timeout=timeout,
        **kwargs
    )

def _post(url: str, headers: dict | None = None, timeout: int = 30, **kwargs):
    return requests.post(
        url=url,
        headers=headers if headers is not None else HDR,
        timeout=timeout,
        **kwargs
    )

def getReport(tid: str, qid: int):
    '''run a report'''
    params = {
        'tableId': tid,
        'skip': '0',
        'top': '400'
    }
    return _post(
        f'https://api.quickbase.com/v1/reports/{qid}/run',
        params=params
    )

def postAttachment(tid: str, payload: dict):
    '''upload an attachment'''
    return _post(
        url="https://api.quickbase.com/v1/records",
        json={"to": tid, "data": payload, "fieldsToReturn": ATTACH_RET_FIDS}
    )

def postFulfillment(tid: str, payload: dict):
    '''upload a fulfillment attachment'''
    return _post(
        url="https://api.quickbase.com/v1/records",
        json={"to": tid, "data": payload, "fieldsToReturn": FULFILL_RET_FIDS}
    )

def getFile(tid: str, rid: str, fid: str, vnum: str):
    '''download an attachment'''
    url=f"https://api.quickbase.com/v1/files/{tid}/{rid}/{fid}/{vnum}"
    log.info("< GET %s", url)
    return _get(
        url=url
    )
