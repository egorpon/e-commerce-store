from django.db import models
from django.contrib.auth.models import User
from store.models import Product


# Create your models here.
class CartItem(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        owner = self.user.username if self.user else f"Guest {self.session_key}"
        return f"{owner} - {self.product.title} X {self.quantity}"
