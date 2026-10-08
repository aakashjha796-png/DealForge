from flask import Flask, render_template, request, jsonify, redirect, url_for
from discount_engine import calculate_deal, calculate_smart_discount
from database import init_db

app = Flask(__name__)

# Initialize database
init_db()


# ==============================
# DEMO PRODUCTS
# ==============================

products = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "category": "Audio",
        "description": "Premium wireless headphones with immersive sound.",
        "price": 2499,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
    },
    {
        "id": 2,
        "name": "Smart Watch",
        "category": "Wearables",
        "description": "Track your fitness, notifications and daily activity.",
        "price": 3499,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30"
    },
    {
        "id": 3,
        "name": "Laptop Backpack",
        "category": "Accessories",
        "description": "Stylish and durable backpack for everyday use.",
        "price": 1799,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62"
    },
    {
        "id": 4,
        "name": "Mechanical Keyboard",
        "category": "Tech",
        "description": "RGB mechanical keyboard built for work and gaming.",
        "price": 2999,
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3"
    },
    {
        "id": 5,
        "name": "Running Shoes",
        "category": "Fashion",
        "description": "Comfortable lightweight shoes for everyday running.",
        "price": 2799,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff"
    },
    {
        "id": 6,
        "name": "Portable Speaker",
        "category": "Audio",
        "description": "Compact speaker with powerful sound and deep bass.",
        "price": 1999,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1"
    }
]


# ==============================
# TEMPORARY CART
# ==============================

cart_items = []


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():

    return render_template(
        "index.html",
        products=products,
        cart_count=len(cart_items)
    )


# ==============================
# CART PAGE
# ==============================

@app.route("/cart")
def cart():

    subtotal = sum(item["price"] for item in cart_items)

    return render_template(
        "cart.html",
        cart_items=cart_items,
        cart_count=len(cart_items),
        subtotal=subtotal
    )


# ==============================
# ADD PRODUCT TO CART
# ==============================

@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):

    for product in products:

        if product["id"] == product_id:

            cart_items.append({
                "name": product["name"],
                "price": product["price"],
                "image": product["image"]
            })

            break

    return redirect(url_for("home"))


# ==============================
# REMOVE PRODUCT FROM CART
# ==============================

@app.route("/remove-from-cart/<int:index>")
def remove_from_cart(index):

    if 0 <= index < len(cart_items):
        cart_items.pop(index)

    return redirect(url_for("cart"))


# ==============================
# CLEAR CART
# ==============================

@app.route("/clear-cart")
def clear_cart():

    cart_items.clear()

    return redirect(url_for("cart"))


# ==============================
# CHECKOUT
# ==============================

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if not cart_items:
        return redirect(url_for("cart"))

    subtotal = sum(item["price"] for item in cart_items)

    is_student = False
    coupon = ""
    discount_result = None

    # When checkout form is submitted
    if request.method == "POST":

        is_student = request.form.get("student") == "yes"

        coupon = request.form.get(
            "coupon",
            ""
        ).strip()

        # Run DealForge smart discount engine
        discount_result = calculate_smart_discount(
            subtotal=subtotal,
            is_student=is_student,
            coupon=coupon
        )

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        cart_count=len(cart_items),
        subtotal=subtotal,
        is_student=is_student,
        coupon=coupon,
        discount_result=discount_result
    )


# ==============================
# BASIC DISCOUNT CALCULATOR
# ==============================

@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.get_json()

    result = calculate_deal(
        original_price=float(data["original_price"]),
        discount=float(data["discount"])
    )

    return jsonify(result)


# ==============================
# START FLASK SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)