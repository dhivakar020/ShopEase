from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product  # Import the Product model

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)  # Include product name in the serializer

    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'cart', 'product', 'product_name', 'quantity']  # Added product_name

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Nested CartItemSerializer

    class Meta:
        model = Cart
        fields = ['cart_id', 'user', 'created_at', 'updated_at', 'items']
