from django.db import models
import uuid
from users.models import Profile, Location, User
from .utils import user_property_directory_path


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
    
    def __str__(self):
        return f'{self.seller.users.username} \'s Listing '
