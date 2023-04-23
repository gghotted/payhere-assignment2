from functools import cached_property

from core.views import WrappedResponseDataMixin
from core.yasg.response import *
from core.yasg.utils import connect_swagger, to_partial_serializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from stores.models import Category, Store
from stores.permissions import IsCategoryOwner, IsStoreOwner
from stores.serializers import (
    CategoryCreateSerializer,
    CategorySerializer,
    CategoryUpdateSerializer,
)


@connect_swagger(
    "get",
    swagger_auto_schema(
        tags=["카테고리"],
        operation_id="카테고리 리스트",
        operation_description="매장의 카테고리 목록을 조회합니다",
        security=[{"Bearer": []}],
        request_body=None,
        responses={
            "200": res200(CategorySerializer(many=True)),
            "401": res401,
            "403": res403,
            "404": res404,
        },
    ),
)
@connect_swagger(
    "post",
    swagger_auto_schema(
        tags=["카테고리"],
        operation_id="카테고리 생성",
        operation_description="매장에 카테고리를 등록합니다",
        security=[{"Bearer": []}],
        request_body=CategoryCreateSerializer(),
        responses={
            "201": res201(CategorySerializer()),
            "400": res400,
            "401": res401,
            "403": res403,
            "404": res404,
        },
    ),
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


@connect_swagger(
    "get",
    swagger_auto_schema(
        tags=["카테고리"],
        operation_id="카테고리 상세",
        operation_description="매장의 카테고리를 조회합니다",
        security=[{"Bearer": []}],
        request_body=None,
        responses={
            "200": res200(CategorySerializer()),
            "401": res401,
            "403": res403,
            "404": res404,
        },
    ),
)
@connect_swagger(
    "patch",
    swagger_auto_schema(
        tags=["카테고리"],
        operation_id="카테고리 수정",
        operation_description="매장의 카테고리를 수정합니다",
        security=[{"Bearer": []}],
        request_body=to_partial_serializer(CategoryUpdateSerializer),
        responses={
            "200": res200(CategorySerializer()),
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
        tags=["카테고리"],
        operation_id="카테고리 삭제",
        operation_description="매장의 카테고리를 삭제합니다",
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
