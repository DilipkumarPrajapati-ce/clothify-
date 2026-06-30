from django.urls import path
from . import views

urlpatterns = [

    # Home Page
    path("", views.home, name="home"),

    # Category Pages
    path("men/", views.men, name="men"),
    path("women/", views.women, name="women"),
    path("kids/", views.kids, name="kids"),

    # Product Details
    path("product/<int:id>/", views.product_detail, name="product_detail"),

    # Cart
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),

    # Wishlist
    path("wishlist/", views.wishlist, name="wishlist"),

    # Login
    path("login/", views.login, name="login"),

    # Social Media
    path("instagram/", views.instagram, name="instagram"),
    path("facebook/", views.facebook, name="facebook"),
    path("youtube/", views.youtube, name="youtube"),
    path("whatsapp/", views.whatsapp, name="whatsapp"),

]