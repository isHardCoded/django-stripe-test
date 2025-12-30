import stripe
from django.conf import settings

def init_stripe(currency="usd"):
    stripe.api_key = settings.STRIPE_KEYS[currency]["secret"]
    return stripe