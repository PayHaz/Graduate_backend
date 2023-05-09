from django.db.models import Max, Min
from rest_framework import serializers
from .models import Category, Product, User, City, ProductFeature, ProductImage


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

    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'images', 'name', 'description', 'price', 'price_suffix', 'is_lower_bound', 'category', 'city_id', 'city_name', 'min_price', 'max_price',)

    def get_images_url(self, obj: Product):
        return [image.image.url for image in obj.images.all()]

    def get_city_id(self, obj: Product):
        return obj.city.id if obj.city else None

    def get_city_name(self, obj: Product):
        return obj.city.name if obj.city else None

    def get_min_price(self, obj):
        min_price_filtered = self.context.get('min_price')
        if min_price_filtered is None:
            # Если значение не передано, то возвращаем минимальную стоимость по умолчанию
            return obj.price
        else:
            return min(obj.price, min_price_filtered)

    def get_max_price(self, obj):
        max_price_filtered = self.context.get('max_price')
        if max_price_filtered is None:
            # Если значение не передано, то возвращаем максимальную стоимость по умолчанию
            return obj.price
        else:
            return max(obj.price, max_price_filtered)


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ('name', 'value')


class ProductCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    features = ProductFeatureSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'price_suffix',
            'is_lower_bound',
            'category',
            'city',
            'features'
        )

    def create(self, validated_data):
        features_data = validated_data.pop('features')
        product = Product.objects.create(**validated_data)
        for feature in features_data:
            ProductFeature.objects.create(product=product, **feature)
        return product




class ProductImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = ProductImage
        fields = ('id', 'images')

    def create(self, validated_data):
        uploaded_images = validated_data.pop("images")
        for image in uploaded_images:
            ProductImage.objects.create(product_id=validated_data['product_id'], image=image)
        return uploaded_images


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user