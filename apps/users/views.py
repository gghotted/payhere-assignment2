from core.views import WrappedResponseDataMixin
from core.yasg.response import *
from core.yasg.utils import connect_swagger, to_partial_serializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import views as jwt_views

from users.serializers import UserCreateSerializer, UserSerializer


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


class TokenCreateAPIView(WrappedResponseDataMixin, jwt_views.TokenObtainPairView):
    pass


class TokenRefreshView(WrappedResponseDataMixin, jwt_views.TokenRefreshView):
    pass


class TokenBlacklistView(WrappedResponseDataMixin, jwt_views.TokenBlacklistView):
    pass
