from functools import cached_property

from core.paginations import DefaultCursorPagination
from core.views import WrappedResponseDataMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from stores.models import Store
from stores.permissions import IsStoreOwner
from stores.serializers import ProductCreateSerializer, ProductSerializer


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
