from datetime import datetime
from html import escape
from pyscript import document

customer_input = document.getElementById("customer")
cash_input = document.getElementById("cash")
error_box = document.getElementById("order-error")
output = document.getElementById("receipt-output")


def money(amount):
    return "₱" + format(amount, ",.2f")


def click(event):
    error_box.textContent = ""

    customer = customer_input.value.strip()
    cash_text = cash_input.value.strip()

    if customer == "" or cash_text == "":
        error_box.textContent = "Enter the buyer's name and the cash amount."
        return

    try:
        cash = float(cash_text)
    except ValueError:
        error_box.textContent = "Cash must be a number."
        return

    # go through each ticket row and add up the ticked ones
    total = 0
    lines = ""
    for row in document.querySelectorAll(".menu-item"):
        if not row.querySelector("input[type=checkbox]").checked:
            continue
        try:
            qty = int(row.querySelector(".qty").value)
        except ValueError:
            qty = 0
        if qty < 1:
            error_box.textContent = "Ticket quantity must be at least 1."
            return
        price = int(row.getAttribute("data-price"))
        name = row.querySelector(".name").textContent
        line_total = price * qty
        total = total + line_total
        lines += (
            '<div class="row"><span>' + str(qty) + " x " + name + "</span>"
            "<span>" + money(line_total) + "</span></div>"
        )

    if total == 0:
        error_box.textContent = "Tick at least one ticket type."
        return
    if cash < total:
        error_box.textContent = "Not enough cash for this total."
        return

    now = datetime.now()

    # swap the plain box for the cute receipt paper
    output.className = "receipt-holder"
    output.innerHTML = (
        '<div class="receipt">'
        '<p class="stars">★ ★ ★ ★ ★</p>'
        "<h3>GUTS TOUR</h3>"
        '<p class="center small">olivia rodrigo ★ ticket booth</p>'
        '<p class="center small">' + now.strftime("%b %d, %Y  %I:%M %p") + "</p>"
        "<hr>"
        '<div class="row"><span>buyer</span><span>' + escape(customer) + "</span></div>"
        '<div class="row"><span>order no.</span><span>#GT-' + now.strftime("%H%M%S") + "</span></div>"
        "<hr>" + lines + "<hr>"
        '<div class="row total"><span>TOTAL</span><span>' + money(total) + "</span></div>"
        '<div class="row"><span>cash</span><span>' + money(cash) + "</span></div>"
        '<div class="row"><span>change</span><span>' + money(cash - total) + "</span></div>"
        "<hr>"
        '<div class="barcode"></div>'
        '<p class="center">thank you for coming ♡</p>'
        '<p class="center small">see you at the show ★</p>'
        "</div>"
    )
