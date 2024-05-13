from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    # image = forms.ImageField()  # Define additional fields outside the Meta class

    class Meta:
        model = Property  # Set the model for the form
        fields = ['property_name', 'color', 'description', 'property_photo', 'property_location', 'price', 'year_built', 'garages', 'plot_size', 'area', 'bathroom', 'bedroom']  # Use a list or tuple
