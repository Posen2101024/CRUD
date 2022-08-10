from django.test import Client, TestCase
from django.urls import reverse


class PingTests(TestCase):
    def test_ping_pong(self):
        client = Client()
        response = client.get(reverse('server:ping'))
        self.assertEqual(200, response.status_code)
