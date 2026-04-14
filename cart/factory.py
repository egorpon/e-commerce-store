import factory
from store.models import Product, Category
from .models import Cart, CartItem
from django.contrib.auth.models import User
from decimal import Decimal


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: f"user_{x}")
    


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda x: f"shoes_{x}")
    slug = factory.Sequence(lambda x: f"shoes-{x}")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Sequence(lambda x: f"vans old school #{x}")
    category = factory.SubFactory(CategoryFactory)
    brand = "Vans"
    description = "Skate shoes"
    slug = factory.Sequence(lambda x: f"vans-old-school-{x}")
    price = Decimal("12.99")
    image = factory.django.ImageField(color="blue", width=100, height=100)


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
