from django.urls import path
from stores.views import StoreDetailAPIView

app_name = "stores"

urlpatterns = [
    path("<int:store_id>/", StoreDetailAPIView.as_view(), name="detail"),
]
