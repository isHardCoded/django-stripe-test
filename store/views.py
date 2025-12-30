from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Item, Order
from .stripe_client import init_stripe

stripe = init_stripe()

def buy_item(request, id):
    item = get_object_or_404(Item, id=id)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.name,
                    "description": item.description,
                },
                "unit_amount": item.price,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:8000/success/",
        cancel_url="http://localhost:8000/cancel/",
    )

    return JsonResponse({"session_id": session.id})

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
    
    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.name,
                    "description": item.description,
                },
                "unit_amount": item.price,
            },
            "quantity": 1,
        } for item in order.items.all()
    ]

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://localhost:8000/success/",
        cancel_url="http://localhost:8000/cancel/",
    )
    
    return JsonResponse({"session_id": session.id})