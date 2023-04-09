from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    city_id = models.IntegerField()
    phone = models.CharField(max_length=30)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    user_id = models.IntegerField()
    status = models.CharField(max_length=30)
    category_id = models.IntegerField()


class Product_feature(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product_id = models.IntegerField()


class Category(models.Model):
    parent_id = models.IntegerField()
    name = models.CharField(max_length=255)


class Product_image(models.Model):
    image_path = models.CharField(max_length=255)
    product_id = models.IntegerField()
    description = models.CharField(max_length=1000)


class City(models.Model):
    name = models.CharField(max_length=255)


