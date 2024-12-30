# serializers.py

from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from django.contrib.auth import get_user_model

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name')
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['order_item_id', 'product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=get_user_model().objects.all())
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = ['order_id', 'user', 'order_status', 'total_price', 'order_date', 'shipping_address', 'city', 'state', 'postal_code', 'country', 'order_items']
