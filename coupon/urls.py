from django.urls import path
from . import views

urlpatterns = [
    path('apply-coupon/', views.apply_discount, name='apply_coupon')
]