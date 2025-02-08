from django.core.validators import RegexValidator
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.CharField(max_length=150, verbose_name='slug', unique=True, validators=[
        RegexValidator(r'[a-z0-9_-]', "slug должен содержать только символы 'a-z', '0-9', '_ -'")])
    image = models.ImageField(upload_to='shop/category/', verbose_name='Изображение', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.slug}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    category = models.ForeignKey('shop.Category', related_name='sub', verbose_name='Категория',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Подкатегория')
    slug = models.CharField(max_length=150, verbose_name='slug', unique=True, validators=[
        RegexValidator(r'[a-z0-9_-]', "slug должен содержать только символы 'a-z', '0-9', '_ -'")])
    image = models.ImageField(upload_to='shop/subcategory/', verbose_name='Изображение', **NULLABLE)

    def __str__(self):
        return f'{self.category} {self.name} {self.slug}'

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
