from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=12, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
            verbose_name_plural = "Shipping Address"

    def __str__(self):
        return "Shipping Address " + str(self.id)