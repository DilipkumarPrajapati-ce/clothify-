from django.db import models
from django.contrib.auth.models import User


# Product Model
class Product(models.Model):

    # Product Name
    name = models.CharField(max_length=200)

    # Selling Price
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Original Price
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Product Description
    description = models.TextField()

    # Category
    category = models.CharField(max_length=100)

    # Product Image
    image = models.ImageField(upload_to='products/')

    # Available Stock
    stock = models.PositiveIntegerField(default=0)

    # Product Rating
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=5.0
    )

    # Discount Percentage
    discount = models.PositiveIntegerField(default=0)

    # Created Date
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Wishlist Model
class Wishlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


# Cart Model
class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

# ==========================
# Order Model
# ==========================

class Order(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=200
    )

    mobile = models.CharField(
        max_length=15
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50,
        default="Cash on Delivery"
    )

    order_status = models.CharField(
        max_length=50,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Order #{self.id} - {self.user.username}"
    # ==========================
# User Profile Model
# ==========================

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_photo = models.ImageField(
        upload_to="profiles/",
        default="profiles/default.png"
    )

    mobile = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username
    

# ==========================
# Product Review
# ==========================

class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    rating = models.PositiveIntegerField(default=5)

    review = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.product.name}" 