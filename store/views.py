from django.shortcuts import get_object_or_404, render

from .models import Category, Product

# Create your views here.


def store(request):
    all_products = (
        Product.objects.all()
        .prefetch_related("discounts", "category__category_discounts")
        .select_related("category")
    )
    context = {"all_products": all_products}
    return render(request, "store/store.html", context=context)


def categories(request):
    all_categories = Category.objects.all()
    return {"all_categories": all_categories}


def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = (
        Product.objects.filter(category=category)
        .prefetch_related("discounts", "category__category_discounts")
        .select_related("category")
    )
    context = {"category": category, "products": products}
    return render(request, "store/list-category.html", context=context)


def product_info(request, product_slug):
    product = (
        Product.objects.filter(slug=product_slug)
        .prefetch_related("discounts", "category__category_discounts")
        .select_related("category")
        .first()
    )
    context = {"product": product}

    return render(request, "store/product-info.html", context=context)
