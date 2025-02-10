from rest_framework import generics
from rest_framework.permissions import AllowAny

from shop.models import Category, Product
from shop.paginators import ShopPaginator
from shop.serializers import CategorySerializer, ProductSerializer


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = ShopPaginator
    permission_classes = [AllowAny]


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = ShopPaginator
    permission_classes = [AllowAny]
