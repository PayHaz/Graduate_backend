from django.urls import path
from app import views


urlpatterns = [
    path('category/tree', views.get_category_tree),
]
