from django.urls import path, include
from app import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserCreateAPIView, UserView


router = DefaultRouter()

urlpatterns = [
    path('category/tree', views.get_category_tree),
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', UserCreateAPIView.as_view(), name='register'),
    path('api/user/', UserView.as_view()),
]