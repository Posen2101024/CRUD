from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class PingTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_ping_pong(self):
        request_url = reverse('server:ping')
        response = self.client.get(request_url)
        self.assertEqual(response.data, 'pong')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
