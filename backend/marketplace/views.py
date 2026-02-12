from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import DeclutterItem
from marketplace.models import Product, Service
from .serializers import (
    DeclutterMarketplaceSerializer,
    ProductMarketplaceSerializer,
    ServiceMarketplaceSerializer,
)


class MarketplaceListView(APIView):
    """
    Unified marketplace listing:
    - Declutter items
    - Products
    - Services

    Only returns items that are:
    - Active
    - Approved by admin
    """

    def get(self, request):
        category = request.query_params.get("category")
        item_type = request.query_params.get("type")

        # -------------------------
        # DECLUTTER ITEMS
        # -------------------------
        declutters = DeclutterItem.objects.filter(
            is_active=True,
            is_approved=True
        )

        if category:
            declutters = declutters.filter(category__slug=category)

        declutter_data = DeclutterMarketplaceSerializer(
            declutters, many=True
        ).data

        # -------------------------
        # PRODUCTS
        # -------------------------
        products = Product.objects.filter(
            is_active=True,
            is_approved=True
        )

        if category:
            products = products.filter(category__slug=category)

        product_data = ProductMarketplaceSerializer(
            products, many=True
        ).data

        # -------------------------
        # SERVICES
        # -------------------------
        services = Service.objects.filter(
            is_available=True,
            is_approved=True
        )

        if category:
            services = services.filter(category__slug=category)

        service_data = ServiceMarketplaceSerializer(
            services, many=True
        ).data

        # -------------------------
        # TYPE FILTERING
        # -------------------------
        if item_type == "declutter":
            return Response(declutter_data)

        if item_type == "product":
            return Response(product_data)

        if item_type == "service":
            return Response(service_data)

        # -------------------------
        # RETURN ALL ITEMS
        # -------------------------
        combined = declutter_data + product_data + service_data

        return Response(combined)
