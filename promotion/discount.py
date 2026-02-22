from store.models import Product
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from .models import Discount
from django.db.models import Q

def get_discounted_price(product: Product) -> Decimal:
    now = timezone.now()

    discount = (
        Discount.objects.filter(
            is_active=True,
            valid_from__lte=now,
            valid_to__gte=now,
        )
        .filter(Q(products=product) | Q(categories=product.category))
        .order_by("-value")
        .first()
    )

    if discount:
        final_price = product.price * (1 - Decimal(discount.value) / 100)
        return final_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return product.price
