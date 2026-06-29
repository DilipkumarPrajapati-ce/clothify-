// =========================
// CLOTHIFY JAVASCRIPT
// =========================

// Navbar Shadow on Scroll
window.addEventListener("scroll", function () {
    const navbar = document.querySelector(".navbar");

    if (navbar) {
        if (window.scrollY > 30) {
            navbar.classList.add("nav-scroll");
        } else {
            navbar.classList.remove("nav-scroll");
        }
    }
});

// Search Box
const searchInput = document.querySelector(".search-box input");

if (searchInput) {
    searchInput.addEventListener("keyup", function () {
        console.log("Searching:", this.value);
    });
}

// Shop Now Button
const shopBtn = document.querySelector(".shop-btn");

if (shopBtn) {
    shopBtn.addEventListener("click", function () {
        window.location.href = "#products";
    });
}

// Wishlist Button
const wishlistBtns = document.querySelectorAll(".wishlist-btn");

wishlistBtns.forEach(btn => {
    btn.addEventListener("click", function () {
        this.classList.toggle("active");

        if (this.classList.contains("active")) {
            this.innerHTML = "❤️ Added";
        } else {
            this.innerHTML = "🤍 Wishlist";
        }
    });
});

// Add To Cart Button
const cartBtns = document.querySelectorAll(".cart-btn");

cartBtns.forEach(btn => {
    btn.addEventListener("click", function () {
        alert("Product Added To Cart");
    });
});

// Buy Now Button
const buyBtns = document.querySelectorAll(".buy-btn");

buyBtns.forEach(btn => {
    btn.addEventListener("click", function () {
        alert("Redirecting To Checkout...");
    });
});

// Newsletter
const newsletter = document.querySelector(".newsletter-form");

if (newsletter) {
    newsletter.addEventListener("submit", function (e) {

        e.preventDefault();

        alert("Thank you for subscribing!");

        newsletter.reset();
    });
}

// Back To Top Button
const topBtn = document.querySelector(".back-to-top");

if (topBtn) {

    window.addEventListener("scroll", function () {

        if (window.scrollY > 300) {
            topBtn.style.display = "block";
        } else {
            topBtn.style.display = "none";
        }

    });

    topBtn.addEventListener("click", function () {

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    });

}