from django.urls import path

from shop.apps import ShopConfig
from shop.views import CategoryListAPIView

app_name = ShopConfig.name

urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
]