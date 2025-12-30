from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Item, Order
from .stripe_client import init_stripe

stripe = init_stripe()

def buy_item(request, id):
    item = get_object_or_404(Item, id=id)

    intent = stripe.PaymentIntent.create(
        amount=item.price,
        currency=item.currency,
        payment_method_types=["card"],
        description=f"Payment for {item.name}"
    )

    return JsonResponse({"client_secret": intent.client_secret})

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(
        request,
        "store/item.html",
        {
            "item": item,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        }
    )

def buy_order(request, id):
    order = get_object_or_404(Order, id=id)

    currency = order.items.first().currency
    amount = sum(item.price for item in order.items.all())

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        payment_method_types=["card"],
        description=f"Payment for Order #{order.id}"
    )

    return JsonResponse({"client_secret": intent.client_secret})