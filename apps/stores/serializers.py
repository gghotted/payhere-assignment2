from core.serializers import CreateSerializer, UpdateSerializer
from core.utils import convert_to_chosung
from rest_framework import serializers

from stores.models import Category, Product, Store


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
        fields = ("name",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "store",
            "name",
        )


class CategoryCreateSerializer(CreateSerializer):
    representation_serializer_class = CategorySerializer

    class Meta:
        model = Category
        fields = ("name",)

    def create(self, validated_data):
        validated_data["store"] = self.context["store"]
        return super().create(validated_data)


class CategoryUpdateSerializer(UpdateSerializer):
    representation_serializer_class = CategorySerializer

    class Meta:
        model = Category
        fields = ("name",)


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "store",
            "category_name",
            "price",
            "cost",
            "name",
            "chosung",
            "description",
            "barcode",
            "sell_by_days",
            "size",
        )

    def get_category_name(self, obj):
        return obj.category.name


class ProductCreateSerializer(CreateSerializer):
    representation_serializer_class = ProductSerializer

    class Meta:
        model = Product
        fields = (
            "category",
            "price",
            "cost",
            "name",
            "description",
            "barcode",
            "sell_by_days",
            "size",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = self.context["store"].categories.all()

    def validate(self, attrs):
        attrs["store"] = self.context["store"]
        Product(**attrs).validate_constraints()  # for unoque_together (name, store)
        return attrs

    def create(self, validated_data):
        validated_data["chosung"] = convert_to_chosung(validated_data["name"])
        return super().create(validated_data)
