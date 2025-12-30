from django.urls import path
from .views import buy_item, item_detail, buy_order

urlpatterns = [
    path("buy_item/<int:id>/", buy_item, name="buy-item"),
    path("buy_order/<int:id>/", buy_order, name="buy-order"),
    path("item/<int:id>/", item_detail, name="item-detail"),
]
