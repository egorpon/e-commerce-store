from django.shortcuts import render
from django.http import JsonResponse
from .models import Coupon
from cart.models import Cart
from cart.cart import CartService
from .discount import get_discount_strategy

# Create your views here.


def apply_discount(request):
    if request.POST.get("action") == "post":
        title = str(request.POST.get("code")).strip()

        try:
            coupon = Coupon.objects.get(title=title, is_active=True)

            if not coupon.is_valid():
                return JsonResponse(
                    {
                        "message": f"This promo code has expired",
                        "status": "danger",
                    }
                )

            request.session["coupon_id"] = coupon.id

            cart = CartService(request)
            strategy = get_discount_strategy(coupon)

            return JsonResponse(
                {
                    "message": f"Promo code applied",
                    "status": "success",
                    "new_total": cart.get_new_total(strategy),
                    "discount_amount": cart.discount_amount(strategy),
                }
            )

        except Coupon.DoesNotExist:
            return JsonResponse(
                {
                    "message": f"Promo code not found",
                    "status": "danger",
                }
            )
