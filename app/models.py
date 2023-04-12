from django.db import models
from django.contrib.auth.models import AbstractUser


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)


class User(AbstractUser):
    city = models.ForeignKey(City, related_name='users', on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE)


class Product(models.Model):
    class ProductStatus(models.TextChoices):
        ACTIVE = 'AC', 'Активен'
        ARCHIVED = 'AR', 'В архиве'
        ON_MODERATE = 'MD', 'На модерации'
        CANCELED = 'CN', 'Отклонен'

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    status = models.CharField(max_length=2, choices=ProductStatus.choices, default=ProductStatus.ON_MODERATE)
    author = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductFeature(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d', default='default_image.png')
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    description = models.TextField(blank=True, default='')
