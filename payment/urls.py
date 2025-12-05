from django.urls import path

from . import views


urlpatterns = [
    path("payment-success/", view=views.payment_success, name="payment_success"),
    path("payment-failed/", view=views.payment_failed, name="payment_failed"),
]