import re

from django.contrib import admin
from django.core.exceptions import ValidationError

from shop.models import Category, Subcategory


# class CategoryAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         reg = re.compile(r'[a-z0-9_-]')
#         if not bool(reg.match(obj.slug)):
#             raise ValidationError("slug должен содержать только символы 'a-z', '0-9', '_ -'")
#         super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'category')
