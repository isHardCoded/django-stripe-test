from django.contrib import admin
from .models import Item, Order

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    list_display_links = ("id", "name")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total_price")
    filter_horizontal = ("items",)