from datetime import timedelta

import factory
from django.utils import timezone

from .models import Coupon


class CouponFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Coupon

    title = "Test"
    type = "Percent"
    value = 12
    is_active = True
    valid_from = factory.LazyFunction(timezone.now)
    valid_to = factory.LazyFunction(lambda: timezone.now() + timedelta(days=7))
