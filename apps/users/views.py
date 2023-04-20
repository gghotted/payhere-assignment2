from core.views import WrappedResponseDataMixin
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import views as jwt_views

from users.serializers import UserCreateSerializer


class UserCreateAPIView(WrappedResponseDataMixin, CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class TokenCreateAPIView(WrappedResponseDataMixin, jwt_views.TokenObtainPairView):
    pass


class TokenRefreshView(WrappedResponseDataMixin, jwt_views.TokenRefreshView):
    pass


class TokenBlacklistView(WrappedResponseDataMixin, jwt_views.TokenBlacklistView):
    pass
