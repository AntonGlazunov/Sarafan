from rest_framework import serializers

from shop.models import Category, Subcategory


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(source='subcategory_set', many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['slug', 'name', 'image', 'subcategory',]
