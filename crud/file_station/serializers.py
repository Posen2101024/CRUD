from rest_framework import serializers


class GetFileSerializer(serializers.Serializer):
    isdir = serializers.BooleanField(required=True)
    contents = serializers.CharField(required=False)
    files = serializers.ListField(required=False)
