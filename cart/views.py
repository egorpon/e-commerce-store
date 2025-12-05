from django.shortcuts import render

from .cart import CartService
from store.models import Product
from django.shortcuts import get_object_or_404

from django.http import JsonResponse
# Create your views here.


def cart_summary(request):
    cart = CartService(request)
    return render(request, "cart/cart-summary.html", {"cart": cart})


def cart_add(request):
    cart = CartService(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))

        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, product_quantity=product_quantity)

        cart_quantity = cart.__len__()

        response = JsonResponse({"cart_quantity": cart_quantity})

        return response


def cart_delete(request):
    cart = CartService(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))

        cart.delete(product_id)

        cart_quantity = cart.__len__()

        cart_total = cart.get_total()

        response = JsonResponse({"quantity": cart_quantity, "total": cart_total})
        return response


def cart_update(request):
    cart = CartService(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))
        cart.update(product_id, product_quantity)

        cart_quantity = cart.__len__()

        cart_total = cart.get_total()

        item_total = cart.get_item_total(product_id)

        response = JsonResponse(
            {
                "quantity": cart_quantity,
                "total": cart_total,
                "item_total": item_total,
            }
        )

        return response
