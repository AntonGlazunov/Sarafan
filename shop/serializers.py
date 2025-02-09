from rest_framework import serializers

from shop.models import Category, Subcategory, Product


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(source='subcategory_set', many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['slug', 'name', 'image', 'subcategory',]


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'name']

class SubcategoryForProductSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer()
    class Meta:
        model = Subcategory
        fields = ['name', 'slug', 'category']

class ProductSerializer(serializers.ModelSerializer):
    subcategory = SubcategoryForProductSerializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'slug', 'subcategory', 'price', 'images']

    def get_images(self, instance):
        images_list = [str(instance.image), str(instance.image1), str(instance.image2)]
        return images_list