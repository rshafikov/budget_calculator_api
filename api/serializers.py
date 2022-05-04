from rest_framework import serializers

from .models import Category, Record, User


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('title', )


class RecordSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField(required=False)
    # user = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('amount', 'user', 'category', 'created')
        model = Record


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')