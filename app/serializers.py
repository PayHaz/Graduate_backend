from rest_framework import serializers
from .models import Category, Product, User, City


class CategoryHierarchySerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    title = serializers.CharField(source='name')
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('value', 'title', 'children',)

    def get_children(self, obj):
        return CategoryHierarchySerializer(obj.children, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images_url')
    price_suffix = serializers.CharField(source='get_price_suffix_display')
    city_id = serializers.SerializerMethodField('get_city_id')
    city_name = serializers.SerializerMethodField('get_city_name')

    class Meta:
        model = Product
        fields = ('id', 'images', 'name', 'description', 'price', 'price_suffix', 'is_lower_bound', 'category', 'city_id', 'city_name',)

    def get_images_url(self, obj: Product):
        return [image.image.url for image in obj.images.all()]

    def get_city_id(self, obj: Product):
        return obj.city.id if obj.city else None

    def get_city_name(self, obj: Product):
        return obj.city.name if obj.city else None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'city', 'phone')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'city', 'phone')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            city=validated_data['city'],
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user