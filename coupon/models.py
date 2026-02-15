from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.


class Coupon(models.Model):
    class TypeChoice(models.Choices):
        PERCENT = "Percent"
        FIXED = "Fixed"

    title = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TypeChoice.choices)
    value = models.IntegerField()
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def clean(self):
        if self.type == "Percent" and self.value > 100:
            raise ValidationError("Percent cannot be greater than 100%")
        if self.value < 0:
            raise ValidationError("Value cannot be less than 0")
        if self.valid_from > self.valid_to:
            raise ValidationError("Valid_to date cannot be earlier than valid_from date")

    def __str__(self):
        return self.title
    
    
    def is_valid(self):
        today = timezone.now().date()
        if not self.valid_from <= today <= self.valid_to:
            return False
        return True
        