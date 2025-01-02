from django.urls import path
from .views import AddToCartView, GetCartItemsView

urlpatterns = [
    path("addToCart/", AddToCartView.as_view(), name="add_to_cart"),
    path('getCartItems/', GetCartItemsView.as_view(), name='get-cart-items'),
]
