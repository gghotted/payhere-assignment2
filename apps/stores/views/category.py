from functools import cached_property

from core.views import WrappedResponseDataMixin
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from stores.models import Store
from stores.permissions import IsStoreOwner
from stores.serializers import CategoryCreateSerializer, CategorySerializer


class CategoryListCreateAPIView(WrappedResponseDataMixin, ListCreateAPIView):
    permission_classes = [IsStoreOwner]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CategoryCreateSerializer
        return CategorySerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['store'] = self.store
        return ctx

    @cached_property
    def store(self):
        obj = get_object_or_404(Store, id=self.kwargs["store_id"])
        self.check_object_permissions(self.request, obj)
        return obj
