import re

from django.contrib import admin
from django.core.exceptions import ValidationError

from shop.models import Category, Subcategory, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'category')


class ProductAdmin(admin.ModelAdmin):
    exclude = ['image1', 'image2']
    list_display = ('slug', 'name', 'subcategory')

admin.site.register(Product, ProductAdmin)
