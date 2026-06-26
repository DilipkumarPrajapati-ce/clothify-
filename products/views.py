from django.shortcuts import render 
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.shortcuts import redirect
from .models import Product, Cart
# Create your views here.
# Create your views here.


from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {
        "products": products
    })


def men(request):
    return render(request,'men.html')

def women(request):
    return render(request,'women.html')

def kids(request):
    return render(request,'kids.html')

from django.shortcuts import render

def cart(request):
    return render(request, 'cart.html')

def wishlist(request):
    return render(request,'wishlist.html')

def login(request):
    return render(request,'login.html')

def instagram(request):
    return render(request,'instagram.html')

def facebook(request):
    return render(request,'facebook.html')

def youtube(request):
    return render(request,'youtube.html')

def whatsapp(request):
    return render(request,'whatsapp.html')

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product_detail.html", {"product": product})

from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, id):

    product = Product.objects.get(id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("home")

@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total": total
        }
    )