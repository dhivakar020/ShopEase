from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id','category_name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    product_image = serializers.ImageField(required=False)  # Include ImageField for product images

    class Meta:
        model = Product
        fields = [
            'product_id',
            'product_name',
            'description',
            'price',
            'stock_quantity',
            'product_image',  
            'category',
            'category_id',
            'created_at',
            'updated_at',
        ]