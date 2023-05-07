from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.parsers import FileUploadParser, MultiPartParser

from .models import Category, Product, User, City
from .serializers import CategoryHierarchySerializer, CategorySerializer, ProductSerializer, UserCreateSerializer, UserSerializer, CitySerializer, ProductCreateSerializer, ProductImageSerializer


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


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def list(self, request, **kwargs):
        queryset = self.get_queryset()

        # проверяем наличие jwt токена
        if request.user.is_authenticated:
            # получаем пользователя из токена
            user = request.user
            queryset = queryset.filter(author=user)
        else:
            # если пользователь не аутентифицирован, то фильтруем по x-city-id
            if 'x-city-id' in request.headers:
                queryset = queryset.filter(city_id=int(request.headers['x-city-id']))
            else:
                # если x-city-id не передан, то выводим все продукты
                pass

        # получаем значение параметра status из URL
        status = request.query_params.get('status', 'ACTIVE')

        # фильтруем по статусу
        queryset = queryset.filter(status=status).order_by('-created_at')[:20]
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)




class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['POST'])
@parser_classes([MultiPartParser, FileUploadParser])
def upload_product_images(request, product_id):
    serializer = ProductImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(product_id=product_id)
        return Response(status=201)
    else:
        return Response(status=400)


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

