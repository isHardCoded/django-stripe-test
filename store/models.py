from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.IntegerField(verbose_name="Price (cents)", help_text="Price in cents, e. g. 1000 = $10.00")

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.price for item in self.items.all())