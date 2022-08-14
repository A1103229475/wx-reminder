import json

import requests
from configs.config import proxies


def request(method: str, url: str, data: dict = {}, timeout: int = 10):
    if not method or not url:
        return None
    if method == 'get':
        return requests.get(url, timeout=timeout)   # , proxies=proxies
    elif method == 'post':
        return requests.post(url, data=json.dumps(data), timeout=timeout)   # , proxies=proxies
    else:
        return None