from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, Wishlist, Order
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import Product, Cart, Wishlist, Order, Profile

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

 # ==========================
# Increase Cart Quantity
# ==========================

def increase_quantity(request, id):

    cart_item = Cart.objects.get(id=id)

    cart_item.quantity += 1

    cart_item.save()

    return redirect("cart")


# ==========================
# Decrease Cart Quantity
# ==========================

def decrease_quantity(request, id):

    cart_item = Cart.objects.get(id=id)

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()

    return redirect("cart")


# ==========================
# Remove Product From Cart
# ==========================

def remove_from_cart(request, id):

    cart_item = Cart.objects.get(id=id)

    cart_item.delete()

    return redirect("cart")  

# ==========================
# Checkout Page
# ==========================

@login_required
def checkout(request):

    # User Cart

    cart_items = Cart.objects.filter(user=request.user)

    # Grand Total

    total = 0

    for item in cart_items:

        total += item.product.price * item.quantity

    # ==========================
    # Place Order
    # ==========================

    if request.method == "POST":

        Order.objects.create(

            user=request.user,

            full_name=request.POST.get("full_name"),

            mobile=request.POST.get("mobile"),

            address=request.POST.get("address"),

            city=request.POST.get("city"),

            state=request.POST.get("state"),

            pincode=request.POST.get("pincode"),

            total_price=total,

            payment_method=request.POST.get("payment_method")

        )

        # Empty Cart After Order

        cart_items.delete()

        # Success Message

        messages.success(
            request,
            "🎉 Your Order has been placed successfully."
        )

        return redirect("home")

    # Checkout Page

    return render(

        request,

        "checkout.html",

        {

            "cart_items": cart_items,

            "total": total

        }

    )

# ==========================
# My Orders
# ==========================

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "my_orders.html",
        {
            "orders": orders
        }
    )

# ==========================
# Order Details
# ==========================

@login_required
def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    return render(
        request,
        "order_detail.html",
        {
            "order": order
        }
    )


# ==========================
# Admin Dashboard
# ==========================

@staff_member_required
def admin_dashboard(request):

    total_users = User.objects.count()

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    total_cart = Cart.objects.count()

    total_wishlist = Wishlist.objects.count()

    revenue = 0

    for order in Order.objects.all():

        revenue += order.total_price

    return render(

        request,

        "admin_dashboard.html",

        {

            "users": total_users,

            "products": total_products,

            "orders": total_orders,

            "cart": total_cart,

            "wishlist": total_wishlist,

            "revenue": revenue

        }

    )
# ==========================
# Admin Products
# ==========================

@staff_member_required
def admin_products(request):

    products = Product.objects.all().order_by("-id")

    return render(
        request,
        "admin_products.html",
        {
            "products": products
        }
    )

# ==========================
# Profile Page
# ==========================

@login_required
def profile(request):

    profile = Profile.objects.get(user=request.user)

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )