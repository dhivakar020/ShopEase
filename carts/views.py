import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, CartItem

class AddToCartView(APIView):
    def post(self, request):
        # token extraction from the request header
        token = request.headers.get("Authorization", "").split("Bearer ")[-1]

        if not token:
            return Response({"error": "Token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # decoding and getting the user id from jwt
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        # getting the use object
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = get_object_or_404(User, id=user_id)

        # Extracting the  product details from the request body
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id)

        # Get or creating new the cart for the user
        cart, created = Cart.objects.get_or_create(user=user)

        # Checking if the product already exists in the cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        # the item should be removed from the table if reaches zero
        if cart_item.quantity <= 0:
            cart_item.delete()
            return Response({
                "message": "Product removed from cart as quantity reached 0",
                "product_name": product.product_name,
            }, status=status.HTTP_200_OK)

        cart_item.save()

        return Response({
            "message": "Product added to cart",
            "cart_item": {
                "product_name": product.product_name,
                "quantity": cart_item.quantity,
                "total_price": cart_item.total_price(),
            },
        }, status=status.HTTP_201_CREATED)




class GetCartItemsView(APIView):
    def get(self, request):
         # Extracting the  product details from the request body
        token = request.headers.get("Authorization", "").split("Bearer ")[-1]

        if not token:
            return Response({"error": "Token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # decoding and getting the user id from jwt
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the cart of the user
        cart = get_object_or_404(Cart, user_id=user_id)

        # Geting all the items in the cart
        cart_items = CartItem.objects.filter(cart=cart)

        # Preparing for the the response data
        items_data = []
        for item in cart_items:
            product = item.product
            items_data.append({
                "product_id": product.product_id,
                "product_name": product.product_name,
                "description": product.description,
                "price": float(product.price),
                "stock_quantity": product.stock_quantity,
                "product_image": product.product_image.url if product.product_image else None,
                "quantity": item.quantity,
                "total_price": float(item.total_price())
            })

        return Response({"cart_items": items_data}, status=status.HTTP_200_OK)