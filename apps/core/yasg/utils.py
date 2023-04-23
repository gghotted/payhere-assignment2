from typing import Type

from django.utils.decorators import method_decorator
from rest_framework.serializers import Serializer


def connect_swagger(method, swagger_schema):
    return method_decorator(swagger_schema, method)


def to_partial_serializer(serializer: Type[Serializer]):
    """
    모든 필드의 required를 False로 바꿉니다
    patch method에 활용합니다
    """
    Meta = serializer.Meta
    extra_kwargs = {f: {"required": False} for f in Meta.fields}
    NewMeta = type("MetaForPartial", (Meta,), {"extra_kwargs": extra_kwargs})
    return type("Partial%s" % serializer.__name__, (serializer,), {"Meta": NewMeta})
