from django.db import models
import uuid
from users.models import Profile, Location, User
from .utils import user_property_directory_path
from .consts import PROPERTY_TYPES, SOLD_CHOICES

class Property(models.Model):
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=100, blank=False)
    property_photo = models.ImageField(upload_to=user_property_directory_path)
    property_location = models.CharField(max_length=100, blank=False)
    year_built = models.DateField()
    price = models.CharField(max_length=20, blank=False)
    garages = models.BigIntegerField()
    plot_size = models.CharField(max_length=200, blank=False)
    area = models.CharField(max_length=200, blank=False)
    bathroom = models.CharField(max_length=20, blank=False)
    bedroom = models.CharField(max_length=20, blank=False)
    color = models.CharField(max_length=24, default='White')
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(choices=SOLD_CHOICES, default=False)
    
    def __str__(self):
        return f'{self.seller.users.username} \'s Listing '
    

class LikedListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(Property, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.listing.property_name} listing liked by {self.profile.users.username}'
    



class PurchasedProperty(models.Model):
   

    property_name = models.CharField(max_length=100)
    property_type = models.CharField(max_length=5, choices=PROPERTY_TYPES)
    house_type = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, db_index=True)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    size_unit = models.CharField(max_length=20)
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    @property
    def purchase_month(self):
        return self.purchase_date.strftime('%B')

    def __str__(self):
        return f"{self.property_name} in {self.city}"

    class Meta:
        indexes = [
            models.Index(fields=['purchase_date'], name='purchase_date_idx'),
        ]
        verbose_name_plural = "Properties"
