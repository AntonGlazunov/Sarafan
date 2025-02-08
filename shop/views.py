from rest_framework import generics

from shop.models import Category
from shop.paginators import CategoryPaginator
from shop.serializers import CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = CategoryPaginator
