
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Property
from .filters import PropertyFilters
from .forms import PropertyForm
from .models import Property, LikedListing
from users.forms import LocationForm
import logging
from django.http import JsonResponse
from .forms import PropertyEditForm
# from imp import reload


def main_view(request):
    # Get all Property objects
    properties = Property.objects.all()  # This retrieves all the Property records from the database
    # Apply any filtering logic (if needed)
    properties_filter = PropertyFilters(request.GET, queryset=properties)
    # Build the context to pass to the template
    context = {
        'name': 'main', 
        'property_filter': properties_filter  
    }
    
    # Render the template with the updated context
    return render(request, 'views/main.html', context)

def listing_view(request):
    return render(request, 'views/listing.html', {'name': 'listing'})

def about_view(request):
    return render (request, 'views/about.html', {'name': 'about'})

def property_single_view(request):
    return render(request, 'views/property-single.html', {'name' : 'property-single'})

def contact_view(request):
    return render (request, 'views/contact.html', {'name': 'contact'})

def home_view(request):
   # Get the logged-in user's profile
    profile = get_object_or_404(Profile, users=request.user)
    agent = Property.objects.all()
    # Retrieve the photo's URL (it returns a relative path to the media root)
    photo_url = profile.photo.url if profile.photo else None
    return render (request, "views/home.html", 
                   context = {
        'photo_url': photo_url,
    
    })
    

@login_required
def property_views(request):
    properties = Property.objects.all()
    properties_filter = PropertyFilters(request.GET, queryset=properties)
    user_liked_listings =  LikedListing.objects.filter(profile=request.user.profile).values_list('listing')
    liked_listing_ids = [l[0] for l in user_liked_listings]
    context = {
        # 'listings': listings,
        'property_filter': properties_filter,
         'liked_listing_ids': liked_listing_ids,
    }
    
    return render(request, "views/property_list.html",  context)

def main_view(request):
    properties = Property.objects.all()
    properties_filter = PropertyFilters(request.GET, queryset=properties)
    context = {
        # 'listings': listings,
        'property_filter': properties_filter
    }
    return render(request, 
    
                  "views/main.html",   context)

def aboutus_view(request):
    return render(request, "views/about-us.html", {"name": "aboutus"})

def contact_view(request):
    return render(request, "views/contact-us.html", {"name": "contact"})

def products_view(request):
    return render(request, "pages/products.html", {"name": "products"})


@login_required
def property_add_view(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)
        location_form = LocationForm(request.POST)
        
        print(f"Property form is valid: {property_form.is_valid()}")
        print(f"Location form is valid: {location_form.is_valid()}")
        
        if property_form.is_valid() and location_form.is_valid():
            try:
                property_location = location_form.save()
                print(f"Location saved with id: {property_location.id}")
                
                property = property_form.save(commit=False)
                property.seller = request.user.profile
                property.location = property_location
                property.save()
                print(f"Property saved with id: {property.id}")
                
                messages.success(request, f'{property.property_name} Property Posted Successfully!')
                return redirect('home')
            except Exception as e:
                logging.exception("Error occurred while saving property")
                messages.error(request, f'An error occurred while posting the Property: {str(e)}')
        else:
            print("Form errors:")
            print(property_form.errors)
            print(location_form.errors)
            messages.error(request, 'Please correct the errors in the form.')
    else:
        property_form = PropertyForm()
        location_form = LocationForm()
    
    return render(request, 'views/property_add.html', {
        'property_form': property_form, 
        'location_form': location_form,
    })

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# @login_required
def listing_view(request, id):
    try:
        logger.debug(f"Received ID: {id}")  # Log the ID that was passed
        property = Property.objects.get(id=id)
        logger.debug(f"Property Found: {property}")  # Log the found property
        return render(request, 'views/property-single.html', {'property_listing': property})
    except Property.DoesNotExist:
        messages.error(request, f'Invalid UUID {id} was provided for property.')
        return redirect('home')
    except Exception as e:
        logger.error(f"An error occurred: {e}")  # Log general exceptions
        return redirect('home')
    
@login_required
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = PropertyEditForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_list')
    else:
        form = PropertyEditForm(instance=property)
    
    logging.debug(f"Form fields: {form.fields}")  # Debugging print
    return render(request, 'views/edit_property.html', {'sold_form': form, 'property': property})
    
@login_required
def edit_view(request, id):
    try:
        property = Property.objects.get(id=id)
        
        if property is None:
            raise Exception
        if request.method == 'POST':
            pass
        else:
            pass 
    except Exception as e:
        messages.error(request, f'An error has occured while trying to edit  the property.')
        return redirect('home')
    
    
@login_required
def like_listing_view(request, id):
    print("Listing ID:", id)  # Print the id parameter
    listing = get_object_or_404(Property, id=id)
    liked_listing, created  = LikedListing.objects.get_or_create(profile=request.user.profile, listing=listing)

    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()
    return JsonResponse({
        'is_liked_by_user': created,
    })
    
    
@login_required
def sold_properties_view(request):
    properties = Property.objects.filter(is_sold=True)
    properties_filter = PropertyFilters(request.GET, queryset=properties)
    context = {
        'property_filter': properties_filter
    }
    return render(request, "views/sold_properties.html", context)
    
@login_required
def edit_view(request, id):
    try:
        property_listing = Property.objects.get(id=id)
        if property_listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = PropertyForm(request.POST, request.FILES,instance=property_listing)
            location_form = LocationForm(request.POST, instance=property_listing.location)
            if listing_form.is_valid and location_form.is_valid:
                listing_form.save()
                location_form.save()
                messages.info(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else:
                messages.error(request, f'An error has occured while trying to edit  the listing.')
                # return reload()


        else:
            listing_form = PropertyForm(instance=property_listing)
            location_form = LocationForm(instance=property_listing.location)
        context = {
            'location_form' : location_form,
            'listing_form' : listing_form
        }
        return render(request, 'views/edit.html', context)
    except Exception as e:
        messages.error(request, f'An error has occured while trying to edit  the listing.')
        return redirect('property_list')

