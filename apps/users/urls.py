from django.urls import path

from users.views import UserCreateAPIView

app_name = 'users'

urlpatterns = [
    path('', UserCreateAPIView.as_view(), name='create'),
]
