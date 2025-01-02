from django.db import models
from django.conf import settings
from products.models import Product  


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)  
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)  
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity
