from django.core import validators
from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    filemask = serializers.CharField(required=False)
    size = serializers.DictField(required=False)
    creation_time = serializers.DictField(required=False)
