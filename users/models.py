from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name='имя пользователя')

    def __str__(self):
        return f'{self.username}, {self.pk}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Purchases(models.Model):
    owner = models.ForeignKey('users.User', verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', verbose_name='Продукт', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.user}, {self.product}'

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

