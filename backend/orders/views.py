from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import serializers


from .models import Cart, CartItem
from .serializers import CartSerializer
from marketplace.models import Product
from .models import Order, OrderItem


class AddToCartView(APIView):
    # Only authenticated users can add items to cart
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get product ID and quantity from request body
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))  # Default quantity is 1

        # Retrieve product or return 404 if not found
        product = get_object_or_404(Product, id=product_id)

        # Get user's cart, create one if it doesn't exist
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if product already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        # If item already exists, increase quantity
        # Otherwise, set initial quantity
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        # Save changes to cart item
        cart_item.save()

        # Return success response
        return Response({"message": "Item added to cart"})
    

class ViewCartView(APIView):
    # Only authenticated users can view cart
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get or create user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Serialize cart data including items
        serializer = CartSerializer(cart)

        # Return serialized cart data
        return Response(serializer.data)
    

class RemoveCartItemView(APIView):
    # Only authenticated users can remove cart items
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        # Get specific cart item belonging to the current user
        cart_item = get_object_or_404(CartItem, id=item_id, cart_user=request.user)

        # Delete the cart item
        cart_item.delete()

        # Return confirmation message
        return Response({"message": "Item Removed"})
    


class CheckoutView(APIView):
    # Only authenticated users can checkout
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Retrieve user's cart or return 404 if not found
        cart = get_object_or_404(Cart, user=request.user)

        # Prevent checkout if cart is empty
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        # Get shipping address from request
        shipping_address = request.data.get("shipping_address")

        # Create new order for the user
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address
        )

        total = 0  # Initialize total price

        # Convert each cart item into an order item
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price  # Store current product price
            )

            # Compute total price
            total += item.product.price * item.quantity

        # Update and save total order price
        order.total_price = total
        order.save()

        # Clear all items from cart after successful checkout
        cart.items.all().delete()

        # Return success message
        return Response({"message": "Order placed successfully"})


class OrderItemSerializer(serializers.ModelSerializer):
    # Include product name from related Product model (read-only)
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        # Fields returned for each order item
        fields = ["product_name", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    # Nested serializer to show all order items
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        # Fields returned for each order
        fields = ["id", "status", "total_price", "created_at", "items"]


class UserOrdersView(APIView):
    # Only authenticated users can view their orders
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve user's orders sorted by newest first
        orders = Order.objects.filter(user=request.user).order_by("-created_at")

        # Serialize multiple orders
        serializer = OrderSerializer(orders, many=True)

        # Return serialized order data
        return Response(serializer.data)
