from django.urls import path
from .views import AddToCartView, ViewCartView, RemoveCartItemView
from .views import CheckoutView, UserOrdersView

urlpatterns = [
    path("cart/", ViewCartView.as_view()),
    
    path("cart/add/", AddToCartView.as_view()),
    path("cart/remove/<int:item_id>/", RemoveCartItemView.as_view()),

    path("checkout/", CheckoutView.as_view()),
    path("my-orders/", UserOrdersView.as_view()),
]
