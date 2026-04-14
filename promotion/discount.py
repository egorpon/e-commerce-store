from store.models import Product
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from .models import Discount
from django.db.models import Q

def get_discounted_price(product: Product) -> Decimal:
    now = timezone.now()

    discounts = [] 

    if product:
        discounts += [d for d in product.discounts.all() if d.valid_from <= now <= d.valid_to and d.is_active]

    if product.category:
        discounts += [d for d in product.category.category_discounts.all() if d.valid_from <= now <= d.valid_to and d.is_active]

    discount = max(discounts, key=lambda d: d.value, default=None)
        

    if discount:
        final_price = product.price * (1 - Decimal(discount.value) / 100)
        return round(final_price,2)

    return Decimal(product.price)
