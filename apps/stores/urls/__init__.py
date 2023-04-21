from django.urls import path
from stores.views import StoreDetailAPIView
from stores.views.category import CategoryListCreateAPIView

app_name = "stores"

urlpatterns = [
    path("<int:store_id>/", StoreDetailAPIView.as_view(), name="detail"),
    path("<int:store_id>/categories/", CategoryListCreateAPIView.as_view(), name="list_category"),
]
