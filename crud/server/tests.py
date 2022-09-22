from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class PingTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_ping_pong(self):
        response = self.client.get(reverse('server:ping'))
        self.assertEqual(200, response.status_code)
