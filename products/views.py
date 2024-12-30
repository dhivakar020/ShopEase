from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryListCreateView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # return 400 if category already exists
        category_name = request.data.get('category_name')
        if Category.objects.filter(category_name=category_name).exists():
            return Response({"detail": f"Category '{category_name}' already exists."},
                            status = status.HTTP_400_BAD_REQUEST)
        # if not exists return 201
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        # Check if the request contains a file for `product_image`
        product_image = request.FILES.get('product_image')
        if product_image:
            serializer.initial_data['product_image'] = product_image
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status = status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        
        # Check if the request contains a file for `product_image`
        product_image = request.FILES.get('product_image')
        if product_image:
            serializer.initial_data['product_image'] = product_image


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)   
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"erros": "Product not found"}, status = status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT) 

class ProductByCategoryView(APIView):
    def get(self, request):
        category_name = request.query_params.get('category', None)
        if not category_name:
            return Response({"error": "Category parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the category object
        category = Category.objects.filter(category_name=category_name).first()
        if not category:
            return Response({"error": f"Category '{category_name}' not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch products for the category
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
