from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    file_mask = serializers.CharField(required=False)
    size = serializers.DictField(required=False)
    creation_time = serializers.DictField(required=False)

    def validate(self, data):
        # Delete keys 'size' and 'creation_time' if there are no one.
        if 'size' in data and not data['size']:
            del data['size']
        if 'creation_time' in data and not data['creation_time']:
            del data['creation_time']

        return data
