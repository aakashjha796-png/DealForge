def calculate_smart_discount(subtotal, is_student=False, coupon=""):

    strategies = []

    # No discount
    strategies.append({
        "name": "No Discount",
        "percentage": 0,
        "amount": 0
    })

    # Student discount
    if is_student:

        student_amount = subtotal * 0.05

        strategies.append({
            "name": "Student Discount",
            "percentage": 5,
            "amount": round(student_amount, 2)
        })

    # Coupon discount
    coupon = coupon.upper().strip()

    if coupon == "SAVE20":
        coupon_percentage = 20

    elif coupon == "DEAL10":
        coupon_percentage = 10

    else:
        coupon_percentage = 0

    if coupon_percentage > 0:

        coupon_amount = subtotal * (coupon_percentage / 100)

        strategies.append({
            "name": f"Coupon {coupon}",
            "percentage": coupon_percentage,
            "amount": round(coupon_amount, 2)
        })

    # Find the best discount
    best_discount = max(
        strategies,
        key=lambda strategy: strategy["amount"]
    )

    total_savings = best_discount["amount"]

    final_price = subtotal - total_savings

    return {
        "strategies": strategies,
        "best_discount": best_discount,
        "total_savings": round(total_savings, 2),
        "final_price": round(final_price, 2)
    }


def calculate_deal(original_price, discount):

    discount_amount = original_price * (discount / 100)

    final_price = original_price - discount_amount

    return {
        "original_price": round(original_price, 2),
        "discount_percent": round(discount, 2),
        "discount_amount": round(discount_amount, 2),
        "final_price": round(final_price, 2)
    }