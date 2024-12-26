from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.utils import timezone


# Create your models here.
class ContactModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Contact"

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='Place_images/', blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='destinations')
    created_date = models.DateTimeField(default=now, blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='Package_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='packages')
    created_date = models.DateTimeField(default=now, blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()
    package_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    related_package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    city = models.ForeignKey(District, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    tourist_place = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    adults = models.PositiveIntegerField()
    children = models.PositiveIntegerField(default=0)
    special_request = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking by {self.name} ({self.email})"


class Blog(models.Model):
    name = models.CharField(max_length=200,blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='Blog_images/',blank=True, null=True)
    created_date = models.DateTimeField(default=now,blank=True, null=True)

    def __str__(self):
        return self.name


# Client Reviews
class ClientReview(models.Model):
    client_name = models.CharField(max_length=100, null=True, blank=True)
    client_image = models.ImageField(upload_to='client_images/', null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.client_name} - {self.designation}"


        
# add Folders 
class Folder(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class Gallery(models.Model):
    folder = models.ForeignKey(Folder, related_name='galleries', on_delete=models.CASCADE)
    # description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.folder.name} - {self.description[:50]}"

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery_images/')

    def __str__(self):
        return f"Image for {self.gallery.folder}"
