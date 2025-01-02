from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product  

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True) 

    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'cart', 'product', 'product_name', 'quantity'] 

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  

    class Meta:
        model = Cart
        fields = ['cart_id', 'user', 'created_at', 'updated_at', 'items']
