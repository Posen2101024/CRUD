import requests


CONN_TIMEOUT = 3
READ_TIMEOUT = 10


class API:
    def __init__(self):
        self._url = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def get(self, request_uri, status_code=200):
        response = requests.get(f'{self.url}/{request_uri}', timeout=(CONN_TIMEOUT, READ_TIMEOUT))
        assert response.status_code == status_code
        return response.json()
