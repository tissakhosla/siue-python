'''api calls to quickbase'''

import requests
from .const import HDR

def _call(url: str, headers: dict | None = None, timeout: int = 30, **kwargs):
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
        'top': '100'
    }
    return _call(
        f'https://api.quickbase.com/v1/reports/{qid}/run',
        params=params
    )


def postAttachment(tid: str, payload: dict):
    '''upload an attachment'''
    return _call(
        url="https://api.quickbase.com/v1/records",
        json={"to": tid, "data": payload, "fieldsToReturn": [6,8,9]}
    )
