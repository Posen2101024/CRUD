import os
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from file_station.serializers import GetFileSerializer


BASE_DIR = os.environ['FILES_BASE_DIR']


class File(APIView):
    def get(self, request, path):
        absolute_path = f'{BASE_DIR}/{path}'
        if os.path.isfile(absolute_path):
            with open(absolute_path, 'rb') as fp:
                contents = fp.read()
            serializer = GetFileSerializer({
                    'isdir': False,
                    'contents': contents,
                })
            return Response(serializer.data, status=status.HTTP_200_OK)
        if os.path.isdir(absolute_path):
            serializer = GetFileSerializer({
                    'isdir': True,
                    'files': os.listdir(absolute_path),
                })
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
