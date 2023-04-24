from functools import partial
from typing import Union

from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors.field import InlineSerializerInspector
from drf_yasg.openapi import (
    TYPE_ARRAY,
    TYPE_NUMBER,
    TYPE_OBJECT,
    TYPE_STRING,
    Response,
    Schema,
)
from rest_framework.serializers import BaseSerializer

serializer_inspector = InlineSerializerInspector(
    *[None] * 5, swagger_settings.DEFAULT_FIELD_INSPECTORS
)


def serializer_to_schema(serializer):
    return serializer_inspector.get_schema(serializer)


def cursor_pagaination_schema(schema: Union[Schema, BaseSerializer]):
    if isinstance(schema, BaseSerializer):
        schema = serializer_to_schema(schema)
    return Schema(
        type=TYPE_OBJECT,
        properties={
            "next": Schema(
                type=TYPE_STRING,
                description="다음 페이지의 url(nullable)",
            ),
            "previous": Schema(type=TYPE_STRING, description="이전 페이지의 url(nullable)"),
            "results": Schema(
                type=TYPE_ARRAY,
                description="결과 리스트",
                items=schema,
            ),
        },
    )


def _res_schema(schema=None, code=None, message=None):
    if isinstance(schema, BaseSerializer):
        schema = serializer_to_schema(schema)
    return Schema(
        type=TYPE_OBJECT,
        properties={
            "meta": Schema(
                type=TYPE_OBJECT,
                properties={
                    "code": Schema(
                        type=TYPE_NUMBER,
                        example="%d" % code,
                    ),
                    "message": Schema(
                        type=TYPE_STRING,
                        example=message,
                    ),
                },
            ),
            "data": schema,
        },
    )


res200_schema = partial(_res_schema, code=200, message="ok")
res201_schema = partial(_res_schema, code=201, message="ok")
res400_schema = _res_schema(code=400, message="error message")
res401_schema = _res_schema(code=401, message="error message")
res403_schema = _res_schema(code=403, message="error message")
res404_schema = _res_schema(code=404, message="error message")
