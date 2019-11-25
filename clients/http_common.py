import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from config import conf


class GenericClient:

    def __init__(self, endpoint):

        self.endpoint = endpoint
        self.max_retries = conf.max_retries
        self.backoff_factor = conf.backoff_factor

        with requests.Session() as self.s:
            retries = Retry(
                total=self.max_retries,
                backoff_factor=self.backoff_factor)

            self.s.mount('http://', HTTPAdapter(max_retries=retries))
            self.s.mount('https://', HTTPAdapter(max_retries=retries))

    def get(self, url, params=None, **kwargs):

        if not params:
            params = dict()

        response = self.s.get(url, params=params, **kwargs)

        return response

    def post(self, url, data=None, **kwargs):
        response = self.s.post(url, data=data, **kwargs)

        return response

    def put(self, url, data=None, **kwargs):
        response = self.s.put(url, data=data, **kwargs)

        return response

