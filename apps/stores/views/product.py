from functools import cached_property

from core.paginations import DefaultCursorPagination
from core.views import WrappedResponseDataMixin
from core.yasg.response import *
from core.yasg.utils import connect_swagger, to_partial_serializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from stores.models import Product, Store
from stores.permissions import IsProductOwner, IsStoreOwner
from stores.serializers import (
    ProductCreateSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
)


@connect_swagger(
    "get",
    swagger_auto_schema(
        tags=["상품"],
        operation_id="상품 리스트",
        operation_description="매장의 상품 목록을 조회합니다",
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                "검색 할 문자열, 상품의 이름 또는 초성에서 검색됩니다",
                required=False,
                type=openapi.TYPE_STRING,
            )
        ],
        request_body=None,
        responses={
            "200": res200(cursor_pagaination_schema(ProductSerializer())),
            "401": res401,
            "403": res403,
            "404": res404,
        },
    ),
)
@connect_swagger(
    "post",
    swagger_auto_schema(
        tags=["상품"],
        operation_id="상품 생성",
        operation_description="매장에 상품을 등록합니다",
        security=[{"Bearer": []}],
        request_body=ProductCreateSerializer,
        responses={
            "201": res201(ProductSerializer()),
            "400": res400,
            "401": res401,
            "403": res403,
            "404": res404,
        },
    ),
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


@connect_swagger(
    "get",
    swagger_auto_schema(
        tags=["상품"],
        operation_id="상품 상세",
        operation_description="매장의 상품을 조회합니다",
        security=[{"Bearer": []}],
        request_body=None,
        responses={
            "200": res200(ProductSerializer()),
            "401": res401,
            "403": res403,
            "404": res404,
        },
    ),
)
@connect_swagger(
    "patch",
    swagger_auto_schema(
        tags=["상품"],
        operation_id="상품 수정",
        operation_description="매장의 상품을 수정합니다",
        security=[{"Bearer": []}],
        request_body=to_partial_serializer(ProductUpdateSerializer),
        responses={
            "200": res200(ProductSerializer()),
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
        tags=["상품"],
        operation_id="상품 삭제",
        operation_description="매장의 상품을 삭제합니다",
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
