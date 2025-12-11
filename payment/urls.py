from django.urls import path

from . import views


urlpatterns = [
    path("payment-success/", view=views.payment_success, name="payment_success"),
    path("payment-failed/", view=views.payment_failed, name="payment_failed"),
    path("checkout/", view=views.checkout, name="checkout"),
    path("complete-order/", view=views.complete_order, name="complete_order"),
]
