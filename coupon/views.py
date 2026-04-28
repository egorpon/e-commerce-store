from django.http import JsonResponse

from cart.cart import CartService

from .models import Coupon

# Create your views here.


def apply_discount(request):
    if request.POST.get("action") == "post":
        title = str(request.POST.get("code")).strip()

        if title == "":
            return JsonResponse(
                {
                    "message": "Please enter a correct promo code",
                    "status": "danger",
                }
            )

        coupon = Coupon.objects.filter(title=title, is_active=True).first()

        if not coupon:
            return JsonResponse(
                {
                    "message": "Promo code not found",
                    "status": "danger",
                }
            )

        if not coupon.is_valid():
            return JsonResponse(
                {
                    "message": "This promo code has expired",
                    "status": "danger",
                }
            )

        cart = CartService(request)

        if cart.cart.coupon:
            return JsonResponse(
                {
                    "message": "A promo code is already applied",
                    "status": "danger",
                }
            )

        cart.cart.coupon = coupon
        cart.cart.save()

        return JsonResponse(
            {
                "message": "Promo code applied",
                "status": "success",
                "new_total": cart.get_new_total(),
                "discount_amount": cart.discount_amount(),
            }
        )
