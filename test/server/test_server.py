def test_server_ping(api):
    assert api.get('server/ping') == 'pong'
