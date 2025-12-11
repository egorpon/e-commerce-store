from django.shortcuts import render, redirect
from .forms import ShippingForm
from .models import ShippingAddress, Order, OrderItem
from cart.cart import CartService
from cart.models import Cart, CartItem
from django.http import JsonResponse

# Create your views here.


def checkout(request):
    form = ShippingForm()
    if request.user.is_authenticated:
        shipping = ShippingAddress.objects.filter(user=request.user).first()
        form = ShippingForm(instance=shipping)
        if request.method == "POST":
            form = ShippingForm(request.POST, instance=shipping)
            if form.is_valid():
                shipping_user = form.save(commit=False)
                shipping_user.user = request.user
                shipping_user.save()
                return redirect("checkout")

        return render(request, "payment/checkout.html", {"form": form})

    else:
        return render(request, "payment/checkout.html",{"form": form})


def payment_success(request):
    if request.user.is_authenticated:
        user_cart = Cart.objects.filter(user=request.user).first()
        user_cart.delete()

    else:
        guest_cart = Cart.objects.filter(session_key=request.session.session_key).first()
        guest_cart.delete()
    return render(request, "payment/payment-success.html")


def payment_failed(request):
    return render(request, "payment/payment-failed.html")


def complete_order(request):
    if request.POST.get("action") == "post":
        name = request.POST.get("name")
        email = request.POST.get("email")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")

        shipping_address = "\n".join(
            filter(None, [address1, address2, city, state, zipcode])
        )

        cart = CartService(request)

        total_cost = cart.get_total()

        if request.user.is_authenticated:
            order = Order.objects.create(full_name=name, email=email,shipping_address=shipping_address,amount_paid=total_cost, user=request.user)

            for item in cart:
                OrderItem.objects.create(order = order, product = item["product"], quantity=item["quantity"], price = item["total"], user = request.user)

        else:

            order = Order.objects.create(full_name=name, email=email,shipping_address=shipping_address,amount_paid=total_cost)

            for item in cart:
                OrderItem.objects.create(order = order, product = item["product"], quantity=item["quantity"], price = item["total"]) 
        
        order_success = True

        response = JsonResponse({'success':order_success})

        return response