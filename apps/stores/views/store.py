from core.views import WrappedResponseDataMixin
from core.yasg.response import *
from core.yasg.utils import connect_swagger, to_partial_serializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from stores.models import Store
from stores.permissions import IsStoreOwner
from stores.serializers import (
    MyStoreCreateSerializer,
    StoreSerializer,
    StoreUpdateSerializer,
)


@connect_swagger(
    "get",
    swagger_auto_schema(
        tags=["매장"],
        operation_id="매장 리스트",
        operation_description="유저의 매장 목록을 조회합니다",
        security=[{"Bearer": []}],
        request_body=None,
        responses={
            "200": res200(StoreSerializer(many=True)),
            "401": res401,
        },
    ),
)
@connect_swagger(
    "post",
    swagger_auto_schema(
        tags=["매장"],
        operation_id="매장 생성",
        operation_description="유저의 매장을 등록합니다",
        security=[{"Bearer": []}],
        request_body=MyStoreCreateSerializer(),
        responses={
            "201": res201(StoreSerializer()),
            "400": res400,
            "401": res401,
        },
    ),
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


@connect_swagger(
    "get",
    swagger_auto_schema(
        tags=["매장"],
        operation_id="매장 상세",
        operation_description="매장을 조회합니다",
        security=[{"Bearer": []}],
        request_body=None,
        responses={
            "200": res200(StoreSerializer()),
            "401": res401,
            "403": res403,
            "404": res404,
        },
    ),
)
@connect_swagger(
    "patch",
    swagger_auto_schema(
        tags=["매장"],
        operation_id="매장 수정",
        operation_description="매장을 수정합니다",
        security=[{"Bearer": []}],
        request_body=to_partial_serializer(StoreUpdateSerializer),
        responses={
            "200": res200(StoreSerializer()),
            "400": res400,
            "401": res401,
            "403": res403,
            "404": res404,
        },
    ),
)
@connect_swagger(
    "delete",
    swagger_auto_schema(
        tags=["매장"],
        operation_id="매장 삭제",
        operation_description="매장을 삭제합니다",
        security=[{"Bearer": []}],
        request_body=None,
        responses={
            "204": res204,
            "401": res401,
            "403": res403,
            "404": res404,
        },
    ),
)
class StoreDetailAPIView(WrappedResponseDataMixin, RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsStoreOwner]

    queryset = Store.objects.all()
    lookup_url_kwarg = "store_id"

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return StoreUpdateSerializer
        return StoreSerializer
