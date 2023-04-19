from django.core import validators
from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    filemask = serializers.CharField(required=False)
    size = serializers.SerializerMethodField(required=False)
    creation_time = serializers.SerializerMethodField(required=False)

    VALID_OPERATORS = (
        'eq',
        'gt',
        'lt',
        'ge',
        'le',
    )

    def __pre_check_fields(self, obj):
        if 'size' not in obj:
            return {}

        if obj['size']['operator'] not in self.VALID_OPERATORS:
            raise validators.ValidationError(
                f"Field size.operator has invalid operator {obj['size']['operator']}"
            )

    def get_size(self, obj):
        self.__pre_check_fields(obj)
        return {
            'value': int(obj['size']['value']),
            'operator': obj['size']['operator'],
        }

    def get_creation_time(self, obj):
        self.__pre_check_fields(obj)

        return {
            'value': obj['creation time']['value'],
            'operator': obj['creation time']['operator'],
        }
