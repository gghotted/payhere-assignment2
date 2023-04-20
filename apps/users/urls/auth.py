from django.urls import path
from users.views import TokenCreateAPIView, TokenRefreshView

app_name = 'auth'

urlpatterns = [
    path('tokens/', TokenCreateAPIView.as_view(), name='create_token'),
    path('tokens/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]
