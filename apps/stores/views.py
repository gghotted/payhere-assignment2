from core.views import WrappedResponseDataMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from stores.models import Store
from stores.serializers import MyStoreCreateSerializer, StoreSerializer


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
