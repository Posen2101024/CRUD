import os
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from file_station.serializers import GetFileSerializer


BASE_DIR = os.environ['FILES_BASE_DIR']


class File(APIView):
    def get(self, request, path):
        abs_path = os.path.join(BASE_DIR, path)
        if os.path.isfile(abs_path):
            with open(abs_path, 'rb') as fp:
                contents = fp.read()
            serializer = GetFileSerializer({
                    'isdir': False,
                    'contents': contents,
                })
            return Response(serializer.data, status=status.HTTP_200_OK)
        if os.path.isdir(abs_path):
            serializer = GetFileSerializer({
                    'isdir': True,
                    'files': os.listdir(abs_path),
                })
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, path):
        abs_dir_path = os.path.join(BASE_DIR, path)
        if os.path.isfile(abs_dir_path):
            return Response(status=status.HTTP_409_CONFLICT)
        if 'file' in request.data:
            os.makedirs(abs_dir_path, exist_ok=True)
            file = request.data['file']
            abs_file_path = os.path.join(abs_dir_path, file.name)
            if os.path.exists(abs_file_path):
                return Response(status=status.HTTP_409_CONFLICT)
            with open(abs_file_path, 'wb') as fp:
                fp.write(file.read())
            return Response(status=status.HTTP_201_CREATED)
        if os.path.isdir(abs_dir_path):
            return Response(status=status.HTTP_409_CONFLICT)
        os.makedirs(abs_dir_path)
        return Response(status=status.HTTP_201_CREATED)
