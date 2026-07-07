from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, Wishlist, Order
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import Product, Cart, Wishlist, Order, Profile
from .models import Review 
from .forms import ProfileForm
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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import razorpay

from .models import Cart, Order


@login_required
def checkout(request):

    # User Cart
    cart_items = Cart.objects.filter(user=request.user)

    # Cart Empty Check
    if not cart_items.exists():

        messages.warning(request, "Your cart is empty.")

        return redirect("cart")

    # Calculate Total
    total = 0

    for item in cart_items:

        total += item.product.price * item.quantity

    # Razorpay Client
    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    # Razorpay Order
    payment = client.order.create({
        "amount": int(total * 100),   # Amount in paisa
        "currency": "INR",
        "payment_capture": 1
    })

    # Place Order
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

            payment_method=request.POST.get("payment_method"),

            order_status="Pending"

        )

        # Empty Cart
        cart_items.delete()

        messages.success(
            request,
            "Order placed successfully."
        )

        return redirect("my_orders")

    # Checkout Page
    context = {

        "cart_items": cart_items,

        "total": total,

        "payment": payment,

        "razorpay_key": settings.RAZORPAY_KEY_ID,

    }

    return render(
        request,
        "checkout.html",
        context
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


@login_required
def edit_profile(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile Updated Successfully."
            )

            return redirect("profile")

    else:

        form = ProfileForm(instance=profile)

    return render(
        request,
        "edit_profile.html",
        {
            "form": form
        }
    )


from django.contrib.auth.models import User
from .models import Product, Order

@login_required
def admin_dashboard(request):

    total_users = User.objects.count()

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    pending_orders = Order.objects.filter(
        order_status="Pending"
    ).count()

    completed_orders = Order.objects.filter(
        order_status="Completed"
    ).count()

    revenue = 0

    for order in Order.objects.all():

        revenue += order.total_price

    recent_orders = Order.objects.all().order_by("-created_at")[:10]

    context = {

        "total_users": total_users,

        "total_products": total_products,

        "total_orders": total_orders,

        "pending_orders": pending_orders,

        "completed_orders": completed_orders,

        "revenue": revenue,

        "recent_orders": recent_orders,

    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )


@login_required
def admin_orders(request):

    orders = Order.objects.all().order_by("-created_at")

    return render(
        request,
        "admin_orders.html",
        {
            "orders": orders
        }
    )


@login_required
def update_order(request, id):

    order = get_object_or_404(Order, id=id)

    if request.method == "POST":

        order.order_status = request.POST.get("status")

        order.save()

        messages.success(
            request,
            "Order Status Updated Successfully."
        )

        return redirect("admin_orders")

    return render(
        request,
        "update_order.html",
        {
            "order": order
        }
    )

@login_required
def add_review(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":

        rating = request.POST.get("rating")

        review = request.POST.get("review")

        Review.objects.create(

            user=request.user,

            product=product,

            rating=rating,

            review=review

        )

        messages.success(
            request,
            "Review Added Successfully."
        )

        return redirect("product_detail", id=id)
    
def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    reviews = Review.objects.filter(
        product=product
    ).order_by("-created_at")

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "reviews": reviews
        }
    )

import razorpay
from django.conf import settings

@login_required
def payment_success(request):

    messages.success(
        request,
        "🎉 Payment Successful!"
    )

    return render(
        request,
        "payment_success.html"
    )

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Order

@login_required
def download_invoice(request, id):

    # Get Order
    order = Order.objects.get(id=id, user=request.user)

    # Create PDF Response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Invoice_{order.id}.pdf"'

    # PDF Canvas
    p = canvas.Canvas(response)

    # Title
    p.setFont("Helvetica-Bold", 20)
    p.drawString(180, 800, "CLOTHIFY")

    p.setFont("Helvetica", 12)
    p.drawString(50, 760, f"Invoice No : {order.id}")
    p.drawString(50, 740, f"Customer : {order.full_name}")
    p.drawString(50, 720, f"Mobile : {order.mobile}")
    p.drawString(50, 700, f"Address : {order.address}")
    p.drawString(50, 680, f"City : {order.city}")
    p.drawString(50, 660, f"State : {order.state}")
    p.drawString(50, 640, f"Pincode : {order.pincode}")

    p.drawString(50, 600, f"Payment : {order.payment_method}")
    p.drawString(50, 580, f"Payment Status : {order.payment_status}")
    p.drawString(50, 560, f"Order Status : {order.order_status}")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 510, f"Grand Total : ₹ {order.total_price}")

    p.setFont("Helvetica", 11)
    p.drawString(50, 450, "Thank you for shopping with Clothify!")

    p.showPage()
    p.save()

    return response