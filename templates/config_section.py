import sys
import os
import copy
import importlib
import time
from string import Template
import pytest
import requests
from icecream import ic
import jmespath

{% include 'common_section.py' %}
{% include 'import_section.py' %}

class HttpRequests:
    def __init__(self):
        self.base_url = "{{ base_url }}"
        self.s = requests.session()

    def act(self, _method, _url, _data, _headers):
        _url = f"{self.base_url}{_url}"
        start = time.time()
        if _method == "GET":
            r = self.s.request(method=_method, url=_url, params=_data, headers=_headers)
        else:
            r = self.s.request(method=_method, url=_url, data=_data, headers=_headers)
        # ic(r.url)
        end = time.time()
        time_span_seconds = round(end - start, 3)
        full_data = {"status_code": r.status_code,
                     "time_span": time_span_seconds,
                     "headers": r.headers,
                     "body": r.json(),
                     "url": r.url,
                     "content_length": r.headers.get('content-length', -1),
                     "request_headers": r.request.headers,
                     "data": _data}
        return full_data


class ModuleLevelObject:
    def __init__(self):
        self.http = HttpRequests()
        self.data = {}


@pytest.fixture(scope="module")
def config_module():
    return ModuleLevelObject()

