from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from carts.models import Cart, CartItem
from orders.models import Order, OrderItem
import jwt

class MakeOrderView(APIView):
    def post(self, request):
        # Extracting Authorization the token from the request headers
        token = request.headers.get("Authorization", "").split("Bearer ")[-1]

        if not token:
            return Response({"error": "Token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decoding the JWT toekn to get the user ID
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Fetching  the user's cart
        cart = get_object_or_404(Cart, user_id=user_id)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Checking for stock availability and calculating the total price
        total_price = 0
        for item in cart_items:
            if item.product.stock_quantity < item.quantity:
                return Response({
                    "error": f"Insufficient stock for {item.product.product_name}"
                }, status=status.HTTP_400_BAD_REQUEST)
            total_price += item.product.price * item.quantity

        # Get shipping address from the request
        shipping_address = request.data.get("shipping_address")
        if not shipping_address:
            return Response({"error": "Shipping address is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order and order items
        with transaction.atomic():
            order = Order.objects.create(
                user_id=user_id,
                total_price=total_price,
                order_status="pending",
                shipping_address=shipping_address,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,  # Use price at the time of order
                )
                # Reduce stock quantity
                item.product.stock_quantity -= item.quantity
                item.product.save()

            # Clear the cart
            cart_items.delete()

        return Response({
            "message": "Order placed successfully",
            "order_id": order.order_id,
            "order_details": {
                "total_price": order.total_price,
                "order_status": order.order_status,
                "shipping_address": order.shipping_address,
                "items": [
                    {
                        "product_name": item.product.product_name,
                        "quantity": item.quantity,
                        "price": item.price,
                        "total_price": item.total_price()
                    }
                    for item in order.items.all()
                ]
            }
        }, status=status.HTTP_201_CREATED)


class GetOrderDetailsView(APIView):
    def get(self, request):
        # Extract the token from the request headers
        token = request.headers.get("Authorization", "").split("Bearer ")[-1]

        if not token:
            return Response({"error": "Token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode the JWT to get the user ID
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Fetch orders for the user
        orders = Order.objects.filter(user_id=user_id)

        if not orders.exists():
            return Response({"message": "No orders found for this user"}, status=status.HTTP_404_NOT_FOUND)

        order_details = []
        for order in orders:
            items = OrderItem.objects.filter(order=order)
            item_details = [
                {
                    "product_name": item.product.product_name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "total_price": item.quantity * item.price,
                }
                for item in items
            ]
            order_details.append({
                "order_id": order.order_id,
                "total_price": order.total_price,
                "order_status": order.order_status,
                "order_date": order.order_date,
                "shipping_address": order.shipping_address,
                "items": item_details,
            })

        return Response({"orders": order_details}, status=status.HTTP_200_OK)