from django.urls import path
from stores.views import StoreDetailAPIView
from stores.views.category import CategoryDetailAPIView, CategoryListCreateAPIView
from stores.views.product import ProductDetailAPIView, ProductListCreateAPIView

app_name = "stores"

urlpatterns = [
    path("<int:store_id>/", StoreDetailAPIView.as_view(), name="detail"),
    path(
        "<int:store_id>/categories/",
        CategoryListCreateAPIView.as_view(),
        name="list_category",
    ),
    path(
        "<int:store_id>/categories/<int:category_id>/",
        CategoryDetailAPIView.as_view(),
        name="detail_category",
    ),
    path(
        "<int:store_id>/products/",
        ProductListCreateAPIView.as_view(),
        name="list_product",
    ),
    path(
        "<int:store_id>/products/<int:product_id>/",
        ProductDetailAPIView.as_view(),
        name="detail_product",
    ),
]
