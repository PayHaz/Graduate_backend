from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, ProductImage, ProductFeature, Category, City

admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductFeature)
admin.site.register(Category)
admin.site.register(City)
