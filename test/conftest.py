import pytest
from utils.api import API


def pytest_addoption(parser):
    parser.addoption('--host', default='http://127.0.0.1')
    parser.addoption('--port', default=None)


@pytest.fixture(scope='session', autouse=True)
def network_location(request):
    host = request.config.getoption('host')
    port = request.config.getoption('port')
    if port is None:
        return host
    return f'{host}:{port}'


@pytest.fixture(scope='session', autouse=True)
def api(request):
    server_api = API()
    server_api.url = request.getfixturevalue('network_location')
    return server_api
