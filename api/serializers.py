from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Category, Record, CustomUser


class CategoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name')


class CategoryAdminSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Category
        fields = ('id', 'user', 'category_name')


class RecordAdminSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(
        format="%H:%M %d-%m-%Y",
        read_only=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='category_name'
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Record
        fields = '__all__'


class RecordUserSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(
        format="%H:%M %d-%m-%Y",
        read_only=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='category_name'
    )

    class Meta:
        model = Record
        fields = ('category', 'amount', 'created')


class CustomUserSerializer(UserSerializer):
    records = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'records', 'currency', 'tg_id')


class CustomUserCreateSerializer(UserSerializer):
    # TODO: Impossible to create a user with this serialzer
    class Meta:
        model = CustomUser
        fields = ('username', 'currency', 'tg_id')
