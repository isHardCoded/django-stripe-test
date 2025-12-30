import stripe
from django.conf import settings

def init_stripe():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe