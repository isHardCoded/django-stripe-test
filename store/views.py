from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Item, Order
from .stripe_client import init_stripe

def item_list(request):
    items = Item.objects.all()
    return render(request, "store/item_list.html", {"items": items})

def order_list(request):
    orders = Order.objects.all()
    return render(request, "store/order_list.html", {"orders": orders})

def buy_item(request, id):
    item = get_object_or_404(Item, id=id)
    stripe = init_stripe(item.currency)

    intent = stripe.PaymentIntent.create(
        amount=item.price,
        currency=item.currency,
        payment_method_types=["card"],
        description=f"Payment for {item.name}"
    )

    return JsonResponse({"client_secret": intent.client_secret})

def buy_order(request, id):
    order = get_object_or_404(Order, id=id)

    currency = order.items.first().currency
    stripe = init_stripe(currency)

    base_amount = sum(item.price for item in order.items.all())

    total_discount = sum(d.amount for d in order.discounts.all())
    amount_after_discount = max(base_amount - total_discount, 0)

    total_tax = sum(amount_after_discount * t.percentage / 100 for t in order.taxes.all())
    final_amount = int(amount_after_discount + total_tax)

    intent = stripe.PaymentIntent.create(
        amount=final_amount,
        currency=currency,
        payment_method_types=["card"],
        description=f"Payment for Order #{order.id}"
    )

    return JsonResponse({"client_secret": intent.client_secret})

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(
        request,
        "store/item.html",
        {
            "item": item,
            "stripe_public_key": settings.STRIPE_KEYS[item.currency]["public"],
        }
    )

def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    currency = order.items.first().currency
    return render(
        request,
        "store/order.html",
        {
            "order": order,
            "stripe_public_key": settings.STRIPE_KEYS[currency]["public"],
        }
    )