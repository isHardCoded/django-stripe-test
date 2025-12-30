from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.IntegerField(verbose_name="Price (cents)", help_text="Price in cents, e.g. 1000 = $10.00")
    currency = models.CharField(max_length=3, default="usd", verbose_name="Currency")
    
    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField(help_text="Discount in cents")

class Tax(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.FloatField(help_text="Tax percent, e.g. 5.5")

class Order(models.Model):
    items = models.ManyToManyField(Item)
    discounts = models.ManyToManyField(Discount, blank=True)
    taxes = models.ManyToManyField(Tax, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id}"
