from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from store.models import Product, Category

# Create your models here.


class Discount(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField()
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    products = models.ManyToManyField(Product, blank=True, related_name="discounts")
    categories = models.ManyToManyField(Category, blank=True, related_name="discounts")

    def clean(self):
        if self.value < 0:
            raise ValidationError("Value cannot be less than 0")
        if self.valid_from > self.valid_to:
            raise ValidationError(
                "Valid_to date cannot be earlier than valid_from date"
            )

    def __str__(self):
        return self.name

    def is_valid(self):
        today = timezone.now()
        if not self.valid_from <= today <= self.valid_to:
            return False
        return True
