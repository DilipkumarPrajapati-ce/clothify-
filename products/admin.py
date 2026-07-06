

# Register your models here.

from django.contrib import admin
from .models import Product, Wishlist, Cart, Order, Profile
from .models import Review

admin.site.register(Review)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Profile)