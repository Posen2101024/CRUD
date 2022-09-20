from rest_framework.views import APIView
from rest_framework.response import Response


class Ping(APIView):
    def get(self, request):
        return Response('pong', status=200)
