import factory
from .models import Discount
from django.utils import timezone
import datetime

class DiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discount

    name = factory.Sequence(lambda x : f'Test_Discount{x}')
    value = 20
    is_active = True
    valid_from = factory.LazyFunction(timezone.now)
    valid_to = factory.LazyFunction( lambda: timezone.now() + datetime.timedelta(days=5))