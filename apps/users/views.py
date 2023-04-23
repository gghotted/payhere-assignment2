from core.views import WrappedResponseDataMixin
from core.yasg.response import *
from core.yasg.utils import connect_swagger
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt import views as jwt_views

from users.serializers import (
    AccessTokenSerializer,
    TokensSerializer,
    UserCreateSerializer,
    UserSerializer,
)


@connect_swagger(
    "post",
    swagger_auto_schema(
        tags=["유저"],
        operation_id="유저 생성",
        operation_description="회원 가입을 합니다",
        security=[{}],
        request_body=UserCreateSerializer(),
        responses={
            "201": res201(UserSerializer()),
            "400": res400,
        },
    ),
)
class UserCreateAPIView(WrappedResponseDataMixin, CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


@connect_swagger(
    "post",
    swagger_auto_schema(
        tags=["인증"],
        operation_id="토큰 생성",
        operation_description="jwt토큰을 생성합니다",
        security=[{}],
        request_body=jwt_serializers.TokenObtainPairSerializer(),
        responses={
            "200": res200(TokensSerializer()),
            "401": res401,
        },
    ),
)
class TokenCreateAPIView(WrappedResponseDataMixin, jwt_views.TokenObtainPairView):
    pass


@connect_swagger(
    "post",
    swagger_auto_schema(
        tags=["인증"],
        operation_id="토큰 리프레시",
        operation_description="access토큰을 리프레시합니다",
        security=[{}],
        request_body=jwt_serializers.TokenRefreshSerializer(),
        responses={
            "200": res200(AccessTokenSerializer()),
            "401": res401,
        },
    ),
)
class TokenRefreshView(WrappedResponseDataMixin, jwt_views.TokenRefreshView):
    pass


@connect_swagger(
    "post",
    swagger_auto_schema(
        tags=["인증"],
        operation_id="리프레시 토큰 폐기",
        operation_description="refresh토큰을 폐기합니다",
        security=[{}],
        request_body=jwt_serializers.TokenBlacklistSerializer(),
        responses={
            "200": res200(Schema(type=TYPE_OBJECT)),
            "401": res401,
        },
    ),
)
class TokenBlacklistView(WrappedResponseDataMixin, jwt_views.TokenBlacklistView):
    pass
