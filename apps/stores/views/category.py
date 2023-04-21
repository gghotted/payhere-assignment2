from functools import cached_property

from core.views import WrappedResponseDataMixin
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from stores.models import Category, Store
from stores.permissions import IsCategoryOwner, IsStoreOwner
from stores.serializers import (
    CategoryCreateSerializer,
    CategorySerializer,
    CategoryUpdateSerializer,
)


class CategoryListCreateAPIView(WrappedResponseDataMixin, ListCreateAPIView):
    permission_classes = [IsStoreOwner]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CategoryCreateSerializer
        return CategorySerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["store"] = self.store
        return ctx

    def get_queryset(self):
        return self.store.categories.all()

    @cached_property
    def store(self):
        obj = get_object_or_404(Store, id=self.kwargs["store_id"])
        self.check_object_permissions(self.request, obj)
        return obj


class CategoryDetailAPIView(WrappedResponseDataMixin, RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsCategoryOwner]
    lookup_url_kwarg = "category_id"

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return CategoryUpdateSerializer
        return CategorySerializer

    def get_queryset(self):
        qs = Category.objects.filter(store_id=self.kwargs["store_id"]).select_related(
            "store"
        )
        return qs
