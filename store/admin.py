from django.contrib import admin
from .models import Item, Order, Discount, Tax

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    list_display_links = ("id", "name")

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "amount")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("amount",)

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "percentage")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("percentage",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total_price_display")
    filter_horizontal = ("items",)

    def total_price_display(self, obj):
        return obj.total_price()
    total_price_display.short_description = "Total Price (cents)"