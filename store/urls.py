from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.store, name="store"),
    path("product/<slug:product_slug>/", view=views.product_info, name="product_info"),
    path("search/<slug:category_slug>/", view=views.list_category, name="list_category"),
]
