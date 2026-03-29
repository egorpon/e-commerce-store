import factory
from .models import Coupon
from django.utils import timezone
from datetime import timedelta


class CouponFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Coupon

    title = "Test"
    type = "Percent"
    value = 12
    is_active = True
    valid_from = factory.LazyFunction(timezone.now)
    valid_to = factory.LazyFunction(lambda: timezone.now() + timedelta(days=7))
