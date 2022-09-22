import os
from unittest.mock import patch, mock_open
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class FileGetTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()

    @patch.object(os, 'listdir', return_value=['file.out', 'file.error'])
    @patch.object(os.path, 'isdir', return_value=True)
    @patch.object(os.path, 'isfile', return_value=False)
    def test_get_exist_dir_200(self, _isfile, _isdir, _listdir):
        response = self.client.get(reverse('file_station:file', kwargs={'path': 'tmp/dir/'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('files' in response.data)
        self.assertEqual(response.data['files'], ['file.out', 'file.error'])
        self.assertTrue('isdir' in response.data)
        self.assertTrue(response.data['isdir'])

    @patch('builtins.open', new_callable=mock_open, read_data='mewmewdata')
    @patch.object(os.path, 'isdir', return_value=False)
    @patch.object(os.path, 'isfile', return_value=True)
    def test_get_exist_file_200(self, _isfile, _isdir, _builtins_open):
        response = self.client.get(reverse('file_station:file', kwargs={'path': 'tmp/file.out'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('contents' in response.data)
        self.assertEqual(response.data['contents'], 'mewmewdata')
        self.assertTrue('isdir' in response.data)
        self.assertFalse(response.data['isdir'])

    @patch.object(os.path, 'isdir', return_value=False)
    @patch.object(os.path, 'isfile', return_value=False)
    def test_get_non_exist_dir_404(self, _isfile, _isdir):
        response = self.client.get(reverse('file_station:file', kwargs={'path': 'mew/dir/'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('builtins.open', new_callable=mock_open, read_data='mewmewdata')
    @patch.object(os.path, 'isdir', return_value=False)
    @patch.object(os.path, 'isfile', return_value=False)
    def test_get_non_exist_file_404(self, _isfile, _isdir, _builtins_open):
        response = self.client.get(reverse('file_station:file', kwargs={'path': 'mew/file.out'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
