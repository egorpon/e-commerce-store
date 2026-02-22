from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q
from store.models import Product, Category
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Discount(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    products = models.ManyToManyField(Product, blank=True, related_name="discounts")
    categories = models.ManyToManyField(Category, blank=True, related_name="category_discounts")

    def clean(self):
        if not self.valid_from or not self.valid_to:
            return
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

 