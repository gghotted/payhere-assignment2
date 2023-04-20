from core.serializers import CreateSerializer, UpdateSerializer
from rest_framework import serializers

from stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            "id",
            "owner",
            "name",
        )


class MyStoreCreateSerializer(CreateSerializer):
    """
    request user에 대한 store 생성
    """

    representation_serializer_class = StoreSerializer

    class Meta:
        model = Store
        fields = ("name",)

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class StoreUpdateSerializer(UpdateSerializer):
    representation_serializer_class = StoreSerializer

    class Meta:
        model = Store
        fields = "name"
