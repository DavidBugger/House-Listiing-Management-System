
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Property
from .filters import PropertyFilters
from .forms import PropertyForm
from users.forms import LocationForm
import logging


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
    context = {
        # 'listings': listings,
        'property_filter': properties_filter
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
        try:
            property_form = PropertyForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST, )
            if property_form.is_valid() and location_form.is_valid():
                property = property_form.save(commit=False)
                property_location = location_form.save()
                property.seller = request.user.profile
                property.location = property_location
                property.save()
                messages.info(
                    request, f'{property.model} Property Posted Successfully!')
                return redirect('property')
            else:
                raise Exception()
        except Exception as e:
            print(e)
            logging.debug(e)
            messages.error(
                request, 'An error occured while posting the Property.')
    elif request.method == 'GET':
        property_form = PropertyForm()
        location_form = LocationForm()
    return render(request, 'views/property_add.html', {'property_form': property_form, 'location_form': location_form,  })

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
