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
    # Add Product To Wishlist
path(
    "add-to-wishlist/<int:id>/",
    views.add_to_wishlist,
    name="add_to_wishlist"
),

    # Login
    path("login/", views.login, name="login"),

    # Social Media
    path("instagram/", views.instagram, name="instagram"),
    path("facebook/", views.facebook, name="facebook"),
    path("youtube/", views.youtube, name="youtube"),
    path("whatsapp/", views.whatsapp, name="whatsapp"),

     # ==========================
# Cart Management
# ==========================

path(
    "cart/increase/<int:id>/",
    views.increase_quantity,
    name="increase_quantity"
),

path(
    "cart/decrease/<int:id>/",
    views.decrease_quantity,
    name="decrease_quantity"
),

path(
    "cart/remove/<int:id>/",
    views.remove_from_cart,
    name="remove_from_cart"
),

# ==========================
# Checkout
# ==========================

path(
    "checkout/",
    views.checkout,
    name="checkout"
),
# ==========================
# My Orders
# ==========================

path(
    "my-orders/",
    views.my_orders,
    name="my_orders"
),

path(
    "order/<int:id>/",
    views.order_detail,
    name="order_detail"
),

path(
    "admin-dashboard/",
    views.admin_dashboard,
    name="admin_dashboard"
),

path(
    "admin-products/",
    views.admin_products,
    name="admin_products"
),

path(
    "profile/",
    views.profile,
    name="profile"
),

path(
    "edit-profile/",
    views.edit_profile,
    name="edit_profile"
),

path(
    "admin-orders/",
    views.admin_orders,
    name="admin_orders"
),

path(
    "update-order/<int:id>/",
    views.update_order,
    name="update_order"
),

path(
    "add-review/<int:id>/",
    views.add_review,
    name="add_review"
),

path(
    "payment-success/",
    views.payment_success,
    name="payment_success"
),


path(
    "invoice/<int:id>/",
    views.download_invoice,
    name="download_invoice"
),













]