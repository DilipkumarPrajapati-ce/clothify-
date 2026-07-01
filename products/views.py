from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product, Cart, Wishlist


# ==========================
# Home Page
# ==========================

# Home Page
def home(request):

    # Search Value
    query = request.GET.get("q")

    # Check Search
    if query:

        products = Product.objects.filter(
            name__icontains=query
        )

    else:

        products = Product.objects.all()

    return render(
        request,
        "home.html",
        {
            "products": products,
            "query": query
        }
    )

# ==========================
# Category Pages
# ==========================

# Men's Products
def men(request):

    products = Product.objects.filter(category__iexact="Men")

    return render(
        request,
        "men.html",
        {
            "products": products
        }
    )


# Women's Products
def women(request):

    products = Product.objects.filter(category__iexact="Women")

    return render(
        request,
        "women.html",
        {
            "products": products
        }
    )


# Kids Products
def kids(request):

    products = Product.objects.filter(category__iexact="Kids")

    return render(
        request,
        "kids.html",
        {
            "products": products
        }
    )
# ==========================
# Static Pages
# ==========================

# ==========================
# Wishlist Page
# ==========================

@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        "wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )

def login(request):
    return render(request, "login.html")


def instagram(request):
    return render(request, "instagram.html")


def facebook(request):
    return render(request, "facebook.html")


def youtube(request):
    return render(request, "youtube.html")


def whatsapp(request):
    return render(request, "whatsapp.html")


# ==========================
# Product Detail
# ==========================

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product_detail.html", {
        "product": product
    })


# ==========================
# Add To Cart
# ==========================

@login_required
def add_to_cart(request, id):

    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

# ==========================
# Add To Wishlist
# ==========================

@login_required
def add_to_wishlist(request, id):

    # Selected Product
    product = get_object_or_404(Product, id=id)

    # Create only if not already present
    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    # Go to wishlist page
    return redirect("wishlist")
# ==========================
# Cart Page
# ==========================

@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })