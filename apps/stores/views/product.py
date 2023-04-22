from functools import cached_property

from core.paginations import DefaultCursorPagination
from core.views import WrappedResponseDataMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from stores.models import Product, Store
from stores.permissions import IsProductOwner, IsStoreOwner
from stores.serializers import (
    ProductCreateSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
)


class ProductListCreateAPIView(WrappedResponseDataMixin, ListCreateAPIView):
    permission_classes = [IsStoreOwner]
    pagination_class = DefaultCursorPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["store"] = self.store
        return ctx

    def get_queryset(self):
        return self.store.products.select_related("category").all()

    def filter_queryset(self, queryset):
        """
        search filter
        """
        search = self.request.GET.get("search")
        if not search:
            return queryset
        return queryset.filter(Q(name__icontains=search) | Q(chosung__icontains=search))

    @cached_property
    def store(self):
        obj = get_object_or_404(Store, id=self.kwargs["store_id"])
        self.check_object_permissions(self.request, obj)
        return obj


class ProductDetailAPIView(WrappedResponseDataMixin, RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsProductOwner]
    lookup_url_kwarg = "product_id"

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return ProductUpdateSerializer
        return ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(store_id=self.kwargs["store_id"]).select_related(
            "category", "store"
        )
