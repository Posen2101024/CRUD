# from rest_framework.decorators import api_view
# from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response


# @api_view(['GET'])
# def ping(request):
#     return Response('pong', status=200)

class Ping(APIView):
    def get(self, request, format=None):
        return Response('pong', status=200)
