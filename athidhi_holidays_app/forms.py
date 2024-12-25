from django import forms
from .models import ContactModel, District, Destination, ClientReview, Gallery, Folder, Blog, Package, Category, Booking



# Contact us
class ContactModelForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'

# District
class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'


# Destination
class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'

# NearByPlaceForm
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

# Clien Review
class ClientReviewForm(forms.ModelForm):
    class Meta:
        model = ClientReview
        fields = '__all__'

# Gallery
class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'

# Folder
class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = '__all__'


# Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


# Package
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

# Booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'start_date', 'end_date', 
                  'package_category', 'related_package', 'city', 'tourist_place', 
                  'adults', 'children', 'special_request']