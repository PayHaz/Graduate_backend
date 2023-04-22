from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Category, Product, User, City
from .serializers import CategoryHierarchySerializer, CategorySerializer, ProductSerializer, UserCreateSerializer, UserSerializer, CitySerializer


@api_view(['GET'])
def get_category_tree(request):
    parent_categories = Category.objects.filter(parent_id=None)
    return Response(CategoryHierarchySerializer(parent_categories, many=True).data)


@api_view(['GET'])
def get_category_list(request):
    parent_categories = Category.objects.filter(parent_id=None)
    return Response(CategorySerializer(parent_categories, many=True).data)


@api_view(['GET'])
def get_city_list(request):
    cities = City.objects.all()
    return Response(CitySerializer(cities, many=True).data)


@api_view(['GET'])
def get_product_list(request):
    products = Product.objects
    if 'x-city-id' in request.headers:
        products = products.filter(city_id=int(request.headers['x-city-id']))
    products = products.filter(status=Product.Status.ACTIVE).order_by('-created_at')[:20]
    return Response(ProductSerializer(products, many=True).data)


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

