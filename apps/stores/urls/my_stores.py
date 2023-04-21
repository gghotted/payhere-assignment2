from django.urls import path
from stores.views import MyStoreListCreateAPIView

app_name = "my_stores"

urlpatterns = [
    path("", MyStoreListCreateAPIView.as_view(), name="list"),
]
