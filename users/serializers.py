from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from shop.models import Product
from users.models import User, Purchases
from users.validators import QuantityValidator


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        user.save()

        return token


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class PurchasesSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='slug'
    )
    quantity = serializers.IntegerField(min_value=0)
    class Meta:
        model = Purchases
        fields = ['product', 'quantity']
        validators = [QuantityValidator(field='quantity')]


class PurchasesAllSerializer(serializers.ModelSerializer):
    purchases_dict = serializers.SerializerMethodField()
    all_quantity = serializers.SerializerMethodField()
    all_price = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['purchases_dict', 'all_quantity', 'all_price']

    def get_purchases_dict(self, instance):
        purchases_dict = {}
        purchases_items = Purchases.objects.filter(owner=instance)
        for purchases_item in purchases_items:
            purchases_dict[purchases_item.product.name] = purchases_item.quantity
        return purchases_dict

    def get_all_quantity(self, instance):
        all_quantity = 0
        purchases_items = Purchases.objects.filter(owner=instance)
        for purchases_item in purchases_items:
            all_quantity += purchases_item.quantity
        return all_quantity

    def get_all_price(self, instance):
        all_price = 0
        purchases_items = Purchases.objects.filter(owner=instance)
        for purchases_item in purchases_items:
            product_price = purchases_item.quantity * purchases_item.product.price
            all_price += product_price
        return all_price