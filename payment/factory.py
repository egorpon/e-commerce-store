import factory

from .models import Order, OrderItem, ShippingAddress


class ShippingAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShippingAddress

    full_name = factory.Faker("name")
    email = factory.Faker("email")
    city = factory.Faker("city")
    address1 = factory.Sequence(lambda x: f"Test st., h. № {x} ")


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem
