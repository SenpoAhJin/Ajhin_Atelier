from rest_framework import serializers
from .models import (
    StoreProfile,
    PortfolioItem,
    StoreListing,
    CommissionRequest,
)



class StoreProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for external seller store profile.
    The owner is automatically assigned from request.user
    """

    class Meta:
        model = StoreProfile
        fields = [
            'id',
            'store_name',
            'description',
            'is_active',
            'created_at'
            
        ]

        read_only_fields = ['id', 'created_at']


class PortfolioItemSerializer(serializers.ModelSerializer):
     """
    Serializer for portfolio items.
    Store is inferred from the authenticated seller.
    """
     
     class Meta:
         model = PortfolioItem
         fields = [
             'id',
             'title',
             'description',
             'created_at'
         ]
         read_only_fields = ['id', 'created_at']


class StoreListingSerializer(serializers.ModelSerializer):
     """
    Serializer for store product/service listings.
    """
     
     class Meta:
         model = StoreListing
         fields = [
             'id', 
             'title',
            'description',
            'listing_type',
            'base_price',
            'is_active',
            'created_at'
         ]

class CommissionRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for customer commission requests.
    Quoted price and status are controlled by the seller.
    """

    class Meta:
        fields = [
            'id',
            'description',
            'quoted_price',
            'status',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'quoted_price',
            'status',
            'created_at'
        ]