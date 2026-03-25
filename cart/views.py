from django.shortcuts import render

from .cart import CartService
from store.models import Product
from django.shortcuts import get_object_or_404

from django.http import JsonResponse

# Create your views here.
from cart.models import CartItem, Cart


def cart_summary(request):
    cart = CartService(request)

    return render(request, "cart/cart-summary.html", {"cart": cart})


def cart_add(request):
    cart_service = CartService(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))

        product = get_object_or_404(Product, id=product_id)

        cart_service.add(product=product, product_quantity=product_quantity)

        cart_quantity = len(cart_service)

        response = JsonResponse(
            {
                "cart_quantity": cart_quantity,
                "message": f"{product.title} added to cart",
                "status": "success",
            }
        )

        return response


def cart_delete(request):
    cart_service = CartService(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))

        cart_service.delete(product_id)

        cart_quantity = len(cart_service)

        cart_total = cart_service.get_total()

        cart_quantity = CartItem.objects.filter(cart=cart_service.cart).count()

        if cart_quantity == 0:
            cart_service.cart.delete()

        response = JsonResponse(
            {
                "quantity": cart_quantity,
                "total": cart_total,
            }
        )
        return response


def cart_update(request):
    cart_service = CartService(request)
    cart = cart_service.cart

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))
        cart_service.update(product_id, product_quantity)

        cart_quantity = len(cart_service)

        cart_total = cart_service.get_total()

        item_total = cart_service.get_item_total(product_id)
        

        if cart.coupon:
            return JsonResponse(
                {
                    "quantity": cart_quantity,
                    "total": cart_total,
                    "item_total": item_total,
                    "discount_amount": cart_service.discount_amount(),
                    "new_total": cart_service.get_new_total(),
                    
                }
            )

        response = JsonResponse(
            {
                "quantity": cart_quantity,
                "total": cart_total,
                "item_total": item_total,
            }
        )

        return response
