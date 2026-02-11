from rest_framework import serializers


# Unified serializer for all marketplace items
# This serializer is used to represent both Products and Services
# in a single, standardized format
class MarketplaceItemSerializer(serializers.Serializer):
    
    # Unique identifier of the item (Product or Service)
    id = serializers.IntegerField()
    
    # Title of the item
    # For Product → this could map from "name"
    # For Service → this maps from "title"
    title = serializers.CharField()
    
    # Price of the item
    # For Product → this could map from "price"
    # For Service → this could map from "base_price"
    # allow_null=True allows flexibility if price is not provided
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        allow_null=True
    )

    # Indicates the type of item (e.g., "product" or "service")
    # Used to distinguish between different marketplace models
    item_type = serializers.CharField()
    
    # Name of the category the item belongs to
    # Optional field (can be null if no category is assigned)
    category = serializers.CharField(allow_null=True)





