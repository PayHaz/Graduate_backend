from rest_framework import serializers
from .models import Category, User


class CategorySerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    title = serializers.CharField(source='name')
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('value', 'title', 'children',)

    def get_children(self, obj):
        return CategorySerializer(obj.children, many=True).data


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