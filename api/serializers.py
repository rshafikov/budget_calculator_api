from rest_framework import serializers

from djoser.serializers import UserSerializer

from .models import Category, Record, User


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='title'
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Record
        fields = '__all__'


class CustomUserSerializer(UserSerializer):
    records = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name','last_name', 'records')
