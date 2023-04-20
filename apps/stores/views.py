from core.views import WrappedResponseDataMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from stores.models import Store
from stores.permissions import IsStoreOwner
from stores.serializers import (
    MyStoreCreateSerializer,
    StoreSerializer,
    StoreUpdateSerializer,
)


class MyStoreListCreateAPIView(WrappedResponseDataMixin, ListCreateAPIView):
    """
    request user에 대한 store list, create
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return MyStoreCreateSerializer
        return StoreSerializer

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class StoreDetailAPIView(WrappedResponseDataMixin, RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsStoreOwner]

    queryset = Store.objects.all()
    lookup_url_kwarg = "store_id"

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return StoreUpdateSerializer
        return StoreSerializer
