from django.urls import path
from users.views import TokenCreateAPIView

app_name = 'auth'

urlpatterns = [
    path('tokens/', TokenCreateAPIView.as_view(), name='create_token'),
]
