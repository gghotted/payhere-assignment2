from core.views import WrappedResponseDataMixin
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import \
    TokenRefreshView as _TokenRefreshView

from users.serializers import UserCreateSerializer


class UserCreateAPIView(WrappedResponseDataMixin, CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class TokenCreateAPIView(WrappedResponseDataMixin, TokenObtainPairView):
    pass


class TokenRefreshView(WrappedResponseDataMixin, _TokenRefreshView):
    pass
