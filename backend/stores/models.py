# Portfolio items showcase previous works
from django.db import models
from accounts.models import ExternalStore
from django.conf import settings

User = settings.AUTH_USER_MODEL

class PortfolioItem(models.Model):
    store = models.ForeignKey(ExternalStore, on_delete=models.CASCADE, related_name="portfolio")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="portfolio/")
    description = models.TextField(blank=True)


    created_at = models.DateTimeField(auto_now_add=True)



# Store listings can be either product or service
class StoreListing(models.Model):
    LISTING_TYPE_CHOICES = (
    ("product", "Product"),
    ("service", "Service"),
    )


    store = models.ForeignKey(ExternalStore, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)


    created_at = models.DateTimeField(auto_now_add=True)

class StoreProfile(models.Model):
    """
    Represents an external seller's store.
    One store per external seller.
    """

    # Owner of the store (external seller)
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='store_profile'
    )

    store_name = models.CharField(max_length=150) # Public-facing store name
    description = models.TextField(blank=True)  # Optional description / bio of the store 
    is_active = models.BooleanField(default=True) # Soft toggle to disable a store without deleting it
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the store was created


    def __str__(self):
        return self.store_name
        

class PortfolioItem(models.Model):
    """
    Portfolio items showcasing seller's previous work
    """
     # Store that owns this portfolio item
    store = models.ForeignKey(
        StoreProfile,
        on_delete=models.CASCADE,
        related_name='portfolio_items'
    )

    title = models.CharField(max_length=150) # Title of the portfolio work
    description = models.TextField(blank=True) # Optional description of the work
    image = models.ImageField(upload_to='porfolio/', blank=True, null=True) # Optional image preview of the work
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the portfolio item was added


    def __str__(self):
        return self.title
    

class StoreListing(models.Model):

    """
    Represents a product or service offered by the store
    """

    LISTING_TYPE_CHOICES = (
        ('product', 'Product'), # Ready-made item
        ('service', 'Service'), # Custom or commission-based work
    )
    # Store that owns this listing
    store = models.ForeignKey(
        StoreProfile,
        on_delete=models.CASCADE,
        related_name='listings'
    )

    title = models.CharField(max_length=150) # Listing title
    description = models.TextField() # Detailed description of the product or service
    # Distinguishes between product vs service
    listing_type = models.CharField(
        max_length=20,
        choices=LISTING_TYPE_CHOICES
    )

    base_price = models.DecimalField(max_digits=10, decimal_places=2) # Starting/base price (especially important for services)
    is_active = models.BooleanField(default=True) # Soft toggle to hide listings without deleting
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the listing was created


    def __str__(self):
        return self.title
    
class CommissionRequest(models.Model):
    """
    Custome Commission request made by a customer

    THIS SHOULD BE IMPLEMENTED AS A UNIQUE PERK (A FKING MUST!!!)
     - ALLOWS TO TRACK THE USERS ACCOUNT THRU IP ADDRESS
     - THIS PERK SHALL BE THE STANDARD SECURITY APPROACH TOWARDS SCAMMERS

     This model handles the full commission lifecycle:
    - Request submission
    - Seller quote
    - Customer decision
    - Completion

    Security & anti-abuse measures (IP tracking, rate limiting, etc.)
    should be handled at the view / middleware level — not directly here.

    """
    STATUS_CHOICES = (
        ('pending', 'Pending'), # Customer submitted request, not reviewed yet
        ('quoted', 'Quoted'), # Seller sent a price/offer
        ('accepted', 'Accepted'), # Customer accepted the quote
        ('rejected', 'Rejected'), # Customer rejected or seller declined
        ('completed', 'Completed'),  # Commission finished and delivered
    )

    # Customer who made the request
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commission_request'
    )
    # Store receiving the commission request
    store = models.ForeignKey(
        StoreProfile,
        on_delete=models.CASCADE,
        related_name='commission_request'
    )
    # Customer's description of the requested work
    description = models.TextField()
     # Price quoted by the seller (nullable until quoted)
    quoted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
   # Current status of the commission request
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )


    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the request was created

    def __str__(self):
        return f"Commission #{self.id} - {self.status}"