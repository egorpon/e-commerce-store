from abc import ABC, abstractmethod
from decimal import Decimal
from .models import Coupon


class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, cart_total_price: Decimal) -> Decimal:
        pass


class PercentageDiscount(DiscountStrategy):
    def __init__(self, value: int):
        self.value = value

    def apply_discount(self, cart_total_price: Decimal) -> Decimal:
        return round(cart_total_price * (1 - Decimal(self.value) / 100), 2)


class FixedDiscount(DiscountStrategy):
    def __init__(self, value: int):
        self.value = Decimal(value)

    def apply_discount(self, cart_total_price: Decimal) -> Decimal:
        return max(Decimal("0.00"), cart_total_price - self.value)


class NoDiscount(DiscountStrategy):
    def apply_discount(self, cart_total_price: Decimal) -> Decimal:
        return cart_total_price


def get_discount_strategy(coupon: Coupon):
    if not coupon:
        return NoDiscount()

    if coupon.type == "Percent":
        return PercentageDiscount(coupon.value)
    elif coupon.type == "Fixed":
        return FixedDiscount(coupon.value)
    return NoDiscount()
