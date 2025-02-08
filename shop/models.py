import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models

from shop.models_services import upload_to_category, upload_to_subcategory, upload_to_product

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.CharField(max_length=150, verbose_name='slug', unique=True, validators=[
        RegexValidator(r'[a-z0-9_-]', "slug должен содержать только символы 'a-z', '0-9', '_ -'")])
    image = models.ImageField(upload_to=upload_to_category, verbose_name='Изображение', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.slug}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    category = models.ForeignKey('shop.Category', verbose_name='Категория',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.CharField(max_length=150, verbose_name='slug', unique=True, validators=[
        RegexValidator(r'[a-z0-9_-]', "slug должен содержать только символы 'a-z', '0-9', '_ -'")])
    image = models.ImageField(upload_to=upload_to_subcategory, verbose_name='Изображение', **NULLABLE)

    def __str__(self):
        return f'{self.category} {self.name} {self.slug}'

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    subcategory = models.ForeignKey('shop.Subcategory', verbose_name='Подкатегория',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.CharField(max_length=150, verbose_name='slug', unique=True, validators=[
        RegexValidator(r'[a-z0-9_-]', "slug должен содержать только символы 'a-z', '0-9', '_ -'")])
    image = models.ImageField(upload_to=upload_to_product, verbose_name='Изображение оригинал', **NULLABLE)
    image1 = models.ImageField(upload_to='shop/product/', verbose_name='Изображение 600*600', **NULLABLE)
    image2 = models.ImageField(upload_to='shop/product/', verbose_name='Изображение 200*200', **NULLABLE)
    price = models.DecimalField(max_digits=1000000, decimal_places=2, verbose_name='Цена')

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            resized_image_600 = img.resize((600, 600), Image.Resampling.LANCZOS)
            buffer = BytesIO()
            resized_image_600.save(buffer, format='JPEG')
            buffer.seek(0)
            base_name = os.path.basename(self.image.name)
            name, ext = os.path.splitext(base_name)
            new_name_600 = f"{self.slug}600{ext}"
            self.image1.save(new_name_600, ContentFile(buffer.read()), save=False)
            buffer.close()
            resized_image_200 = img.resize((200, 200), Image.Resampling.LANCZOS)
            buffer = BytesIO()
            resized_image_200.save(buffer, format='JPEG')
            buffer.seek(0)
            new_name_200 = f"{self.slug}200{ext}"
            self.image2.save(new_name_200, ContentFile(buffer.read()), save=False)
            buffer.close()
        super().save(*args, **kwargs)


