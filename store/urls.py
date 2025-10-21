from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.store, name='store'),
    path('product/<slug:slug>/', view=views.product_info, name='product_info')
]