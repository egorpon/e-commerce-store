from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from decimal import Decimal

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        owner = self.user.username if self.user else self.session_key
        return f"Cart {owner}"
    
    @property
    def total_price(self):
        return sum(item.item_total_price for item in self.items.all())
    
    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

   

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_total_price(self):
        return Decimal(self.product.price) * self.quantity

    def __str__(self):
        return f"{self.product.title} X {self.quantity}"
