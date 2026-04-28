from decimal import Decimal

from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("list_category", args=[self.slug])


class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE, null=True
    )
    brand = models.CharField(max_length=255, default="un-branded")
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return self.title

    @property
    def sell_price(self) -> Decimal:
        from promotion.discount import get_discounted_price

        return get_discounted_price(self)

    @property
    def has_discount(self):
        return self.sell_price < self.price

    @property
    def discount_percent(self):
        if self.has_discount:
            percent = (1 - (self.sell_price / self.price)) * 100
            return round(percent)
        return 0

    def get_absolute_url(self):
        return reverse("product_info", args=[self.slug])
