import os

from rest_framework.views import APIView
from rest_framework.response import Response


class File(APIView):
    def get(self, request, path):
        absolute_path = f"{os.environ['FILES_BASE_DIR']}/{path}"
        if os.path.exists(absolute_path):
            with open(absolute_path, 'rb') as f:
                text = f.read()
            return Response(text, status=200)
        return Response(status=404)
