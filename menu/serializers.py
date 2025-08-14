from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MenuItem, Order


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
   
    items = MenuItemSerializer(many=True, read_only=True)
    items_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MenuItem.objects.all(),
        write_only=True,
        source='items'
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'items_ids', 'created_at']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Sifariş ən azı 1 məhsuldan ibarət olmalıdır.")
        return value
