from django.urls import path
from .views import main_view, listing_view, about_view,property_single_view, contact_view,home_view,property_views,property_add_view
from django.conf.urls.static import static 
from django.conf import settings



urlpatterns = [
    path('', main_view, name = 'main'),
   
    path('about/', about_view, name = 'about'),
    path('property-single/', property_single_view, name = 'property-single'),
    path('contact/', contact_view, name = 'contact'),
    path('home/', home_view, name = 'home'),
    
    path('property_add/', property_add_view, name = 'property_add'),
    path('property/', property_views, name = 'property'),
    path('property_listing/<str:id>/', listing_view, name = 'property_listing'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
