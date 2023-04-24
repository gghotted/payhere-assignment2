from rest_framework import serializers


class CreateSerializer(serializers.ModelSerializer):
    representation_serializer_class = None

    def to_representation(self, instance):
        return self.representation_serializer_class(instance=instance).data


class UpdateSerializer(serializers.ModelSerializer):
    representation_serializer_class = None

    def to_representation(self, instance):
        return self.representation_serializer_class(instance=instance).data
