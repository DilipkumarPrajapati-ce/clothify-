from django.shortcuts import render 
from django.http import HttpResponse

# Create your views here.
# Create your views here.



def home(request):
    return render(request,'home.html')

def men(request):
    return render(request,'men.html')

def women(request):
    return render(request,'women.html')

def kids(request):
    return render(request,'kids.html')

def cart(request):
    return render(request,'cart.html')

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