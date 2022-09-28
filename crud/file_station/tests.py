import os
from unittest.mock import patch, mock_open
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from file_station.views import BASE_DIR


FILE_PATH = os.path.join(os.path.dirname(__file__), 'static/file.out')


class GetFileTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()

    @patch.object(os, 'listdir', return_value=['file.out', 'file.error'])
    @patch.object(os.path, 'isdir', return_value=True)
    @patch.object(os.path, 'isfile', return_value=False)
    def test_get_exist_dir_200(self, mock_isfile, mock_isdir, mock_listdir):
        kwargs = {'path': 'tmp/dir/'}
        request_url = reverse('file_station:file', kwargs=kwargs)
        response = self.client.get(request_url)
        abs_path = os.path.join(BASE_DIR, kwargs['path'])
        mock_isfile.assert_called_once_with(abs_path)
        mock_isdir.assert_called_once_with(abs_path)
        mock_listdir.assert_called_once_with(abs_path)
        self.assertTrue('files' in response.data)
        self.assertEqual(response.data['files'], ['file.out', 'file.error'])
        self.assertTrue('isdir' in response.data)
        self.assertTrue(response.data['isdir'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('builtins.open', new_callable=mock_open, read_data='mewmewdata')
    @patch.object(os.path, 'isdir', return_value=False)
    @patch.object(os.path, 'isfile', return_value=True)
    def test_get_exist_file_200(self, mock_isfile, mock_isdir, mock_builtins_open):
        kwargs = {'path': 'tmp/file.out'}
        request_url = reverse('file_station:file', kwargs=kwargs)
        response = self.client.get(request_url)
        abs_path = os.path.join(BASE_DIR, kwargs['path'])
        mock_isfile.assert_called_once_with(abs_path)
        mock_isdir.assert_not_called()
        mock_builtins_open.assert_called_once_with(abs_path, 'rb')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('contents' in response.data)
        self.assertEqual(response.data['contents'], 'mewmewdata')
        self.assertTrue('isdir' in response.data)
        self.assertFalse(response.data['isdir'])

    @patch.object(os.path, 'isdir', return_value=False)
    @patch.object(os.path, 'isfile', return_value=False)
    def test_get_non_exist_dir_404(self, mock_isfile, mock_isdir):
        kwargs = {'path': 'mew/dir/'}
        request_url = reverse('file_station:file', kwargs=kwargs)
        response = self.client.get(request_url)
        abs_path = os.path.join(BASE_DIR, kwargs['path'])
        mock_isfile.assert_called_once_with(abs_path)
        mock_isdir.assert_called_once_with(abs_path)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(os.path, 'isdir', return_value=False)
    @patch.object(os.path, 'isfile', return_value=False)
    def test_get_non_exist_file_404(self, mock_isfile, mock_isdir):
        kwargs = {'path': 'mew/file.out'}
        request_url = reverse('file_station:file', kwargs=kwargs)
        response = self.client.get(request_url)
        abs_path = os.path.join(BASE_DIR, kwargs['path'])
        mock_isfile.assert_called_once_with(abs_path)
        mock_isdir.assert_called_once_with(abs_path)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostFileTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()

    @patch.object(os, 'makedirs')
    @patch.object(os.path, 'isdir', return_value=True)
    @patch.object(os.path, 'isfile', return_value=False)
    def test_post_dir_exist_path_only_409(self, mock_isfile, mock_isdir, mock_makedirs):
        kwargs = {'path': 'tmp/dir/'}
        request_url = reverse('file_station:file', kwargs=kwargs)
        response = self.client.post(request_url)
        abs_dir_path = os.path.join(BASE_DIR, kwargs['path'])
        mock_isfile.assert_called_once_with(abs_dir_path)
        mock_isdir.assert_called_once_with(abs_dir_path)
        mock_makedirs.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    @patch.object(os, 'makedirs')
    @patch.object(os.path, 'isdir', return_value=False)
    @patch.object(os.path, 'isfile', return_value=True)
    def test_post_file_exist_path_only_409(self, mock_isfile, mock_isdir, mock_makedirs):
        kwargs = {'path': 'tmp/dir/'}
        request_url = reverse('file_station:file', kwargs=kwargs)
        response = self.client.post(request_url)
        abs_dir_path = os.path.join(BASE_DIR, kwargs['path'])
        mock_isfile.assert_called_once_with(abs_dir_path)
        mock_isdir.assert_not_called()
        mock_makedirs.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    @patch.object(os, 'makedirs')
    @patch.object(os.path, 'isdir', return_value=False)
    @patch.object(os.path, 'isfile', return_value=False)
    def test_post_non_exist_path_only_201(self, mock_isfile, mock_isdir, mock_makedirs):
        kwargs = {'path': 'tmp/dir/'}
        request_url = reverse('file_station:file', kwargs=kwargs)
        response = self.client.post(request_url)
        abs_dir_path = os.path.join(BASE_DIR, kwargs['path'])
        mock_isfile.assert_called_once_with(abs_dir_path)
        mock_isdir.assert_called_once_with(abs_dir_path)
        mock_makedirs.assert_called_once_with(abs_dir_path)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(os.path, 'exists', return_value=True)
    @patch.object(os, 'makedirs')
    @patch.object(os.path, 'isdir', return_value=False)
    @patch.object(os.path, 'isfile', return_value=False)
    def test_post_exist_file_name_409(self, mock_isfile, mock_isdir, mock_makedirs, mock_exists):
        kwargs = {'path': 'tmp/dir/'}
        request_url = reverse('file_station:file', kwargs=kwargs)
        abs_dir_path = os.path.join(BASE_DIR, kwargs['path'])
        abs_file_path = os.path.join(abs_dir_path, os.path.basename(FILE_PATH))
        with open(FILE_PATH, 'rb') as fp:
            data = {'file': fp}
            with patch('builtins.open', new_callable=mock_open, read_data='mewmewdata') as mock_builtins_open:
                response = self.client.post(request_url, data, fmt='multipart')
                mock_builtins_open.assert_not_called()
        mock_isfile.assert_called_once_with(abs_dir_path)
        mock_isdir.assert_not_called()
        mock_makedirs.assert_called_once_with(abs_dir_path, exist_ok=True)
        mock_exists.assert_called_once_with(abs_file_path)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    @patch.object(os.path, 'exists', return_value=False)
    @patch.object(os, 'makedirs')
    @patch.object(os.path, 'isdir', return_value=False)
    @patch.object(os.path, 'isfile', return_value=False)
    def test_post_non_exist_file_name_201(self, mock_isfile, mock_isdir, mock_makedirs, mock_exists):
        kwargs = {'path': 'tmp/dir/'}
        request_url = reverse('file_station:file', kwargs=kwargs)
        abs_dir_path = os.path.join(BASE_DIR, kwargs['path'])
        abs_file_path = os.path.join(abs_dir_path, os.path.basename(FILE_PATH))
        with open(FILE_PATH, 'rb') as fp:
            data = {'file': fp}
            with patch('builtins.open', new_callable=mock_open, read_data='mewmewdata') as mock_builtins_open:
                response = self.client.post(request_url, data, fmt='multipart')
                mock_builtins_open.assert_called_once_with(abs_file_path, 'wb')
                fp.seek(0)
                mock_builtins_open().write.assert_called_once_with(fp.read())
        mock_isfile.assert_called_once_with(abs_dir_path)
        mock_isdir.assert_not_called()
        mock_makedirs.assert_called_once_with(abs_dir_path, exist_ok=True)
        mock_exists.assert_called_once_with(abs_file_path)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
