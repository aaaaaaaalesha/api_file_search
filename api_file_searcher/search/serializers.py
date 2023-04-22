from rest_framework import serializers
from django.conf import settings


class SearchSerializer(serializers.Serializer):
    class SizeSerializer(serializers.Serializer):
        value = serializers.IntegerField(required=True)
        operator = serializers.ChoiceField(
            choices=settings.ACCEPTED_OPERATORS,
            default='eq',
        )

    class CreationTimeSerializer(serializers.Serializer):
        value = serializers.DateTimeField(required=True)
        operator = serializers.ChoiceField(
            choices=settings.ACCEPTED_OPERATORS,
            default='eq',
        )

    text = serializers.CharField(required=False)
    file_mask = serializers.CharField(required=False)
    size = SizeSerializer(required=False)
    creation_time = CreationTimeSerializer(required=False)
