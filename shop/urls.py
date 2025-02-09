from django.urls import path

from shop.apps import ShopConfig
from shop.views import CategoryListAPIView, ProductListAPIView

app_name = ShopConfig.name

urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
]