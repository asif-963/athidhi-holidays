from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import random


from .models import ContactModel, District, Destination, ClientReview, Gallery, Folder, GalleryImage, Blog, Category, Package, Booking
from .forms import ContactModelForm, DestinationForm, ClientReviewForm, GalleryForm, FolderForm, BlogForm, DistrictForm, CategoryForm, PackageForm, BookingForm



def index(request):
    reviews = ClientReview.objects.all()
    blogs = Blog.objects.all()
    packages = Package.objects.all()
    return render(request, 'index.html',{'reviews':reviews, 'blogs':blogs, 'packages':packages})


def about(request):
    reviews = ClientReview.objects.all()
    return render(request, 'about.html',{'reviews':reviews})


def destinations(request):
    districts = District.objects.prefetch_related('destinations').all()
    return render(request, 'destinations.html', {'districts': districts})

def destination_details(request, id):
    destination = get_object_or_404(Destination, id=id)
    return render(request, 'destination_details.html', {'destination': destination})

def packages(request):
    categories = Category.objects.prefetch_related('packages').all()
    return render(request, 'packages.html', {'categories': categories})

def package_details(request, id):
    package = get_object_or_404(Package, id=id)
    return render(request, 'package_details.html', {'package': package})

def blogs(request):
    blogs = Blog.objects.all().order_by('-created_date')
    return render(request, 'blogs.html', {'blogs': blogs})

def blog_details(request, blog_id):  # Use blog_id here
    blog = get_object_or_404(Blog, pk=blog_id)  # Use blog_id instead of pk
    recent_posts = Blog.objects.exclude(id=blog_id).order_by('-created_date')[:6] 
    return render(request, 'blog_details.html', {'blog': blog, 'recent_posts':recent_posts})

def gallery(request):
    folders = Folder.objects.prefetch_related('galleries')
    all_images = GalleryImage.objects.all()
    return render(request, 'gallery.html', {'folders': folders, 'all_images': all_images})

def contact(request):
    if request.method == 'POST':
        form = ContactModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been successfully submitted.')
            return redirect('contact')
    else:
        form = ContactModelForm()
    return render(request, 'contact.html', {'form': form})


def booking(request):
    categories = Category.objects.all()
    districts = District.objects.all()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(request, 'Your booking has been successfully submitted.')
            return redirect('booking')
        else:
            print("Form errors:", form.errors)  # Debugging: Print form errors
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form, 'categories': categories, 'districts': districts})




def get_related_packages(request):
    category_id = request.GET.get('category')
    packages = Package.objects.filter(category_id=category_id)
    data = list(packages.values('id', 'name'))
    return JsonResponse(data, safe=False)

def get_tourist_places(request):
    district_id = request.GET.get('district')
    places = Destination.objects.filter(district_id=district_id)
    data = list(places.values('id', 'name'))
    return JsonResponse(data, safe=False)



# Admin Side
@csrf_protect
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, Admin!")
            return redirect('dashboard')  # Redirect to the dashboard
        else:   
            messages.error(request, "There was an error logging in. Please try again.")
            return redirect('user_login')
    return render(request, 'authenticate/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out"))
    return redirect('user_login')


#  dashboard
@login_required(login_url='user_login')
def dashboard(request):
    return render(request,'admin_pages/dashboard.html')


# Contact 
@login_required(login_url='user_login')
def contact_view(request):
    contacts = ContactModel.objects.all().order_by('-id')
    return render(request,'admin_pages/contact_view.html',{'contacts':contacts})

@login_required(login_url='user_login')
def delete_contact(request,id):
    contact = ContactModel.objects.get(id=id)
    contact.delete()
    return redirect('contact_view')



# Booking 
@login_required(login_url='user_login')
def booking_view(request):
    bookings = Booking.objects.all().order_by('-id')
    return render(request,'admin_pages/booking_view.html',{'bookings':bookings})

@login_required(login_url='user_login')
def delete_booking(request,id):
    booking = Booking.objects.get(id=id)
    booking.delete()
    return redirect('booking_view')


# Add Destrict
@login_required(login_url='user_login')
def add_district(request):
    if request.method == 'POST':
        form = DistrictForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_destinations') 
    else:
        form = DistrictForm()

    return render(request, 'admin_pages/add_district.html', {'form': form})

@login_required(login_url='user_login')
def view_districts(request):
    districts = District.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_districts.html', {'districts': districts})

@login_required(login_url='user_login')
def update_district(request, id):
    district = get_object_or_404(District, id=id)
    if request.method == 'POST':
        form = DistrictForm(request.POST, request.FILES, instance=district)
        if form.is_valid():
            form.save()
            return redirect('add_destinations')
    else:
        form = DistrictForm(instance=district)
    return render(request, 'admin_pages/update_district.html', {'district': district, 'district': district})

@login_required(login_url='user_login')
def delete_district(request,id):
    district = District.objects.get(id=id)
    district.delete()   
    return redirect('view_districts')


# Destination
@login_required(login_url='user_login')
def add_destinations(request):
    districts = District.objects.all()
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_destinations') 
    else:
        form = DestinationForm()

    return render(request, 'admin_pages/add_destinations.html', {'form': form, 'districts':districts})


@login_required(login_url='user_login')
def view_destinations(request):
    places = Destination.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_destinations.html', {'places': places})


@login_required(login_url='user_login')
def update_destination(request, id):
    place = get_object_or_404(Destination, id=id)
    districts = District.objects.all()
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            return redirect('view_destinations')
    else:
        form = DestinationForm(instance=place)
    return render(request, 'admin_pages/update_destination.html', {'form': form, 'place': place, 'districts':districts})

@login_required(login_url='user_login')
def delete_destination(request,id):
    places = Destination.objects.get(id=id)
    places.delete()
    return redirect('view_destinations')

# Blog
@login_required(login_url='user_login')
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_blogs') 
    else:
        form = BlogForm()

    return render(request, 'admin_pages/add_blog.html', {'form': form})


@login_required(login_url='user_login')
def view_blogs(request):
    blogs = Blog.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_blogs.html', {'blogs': blogs})


@login_required(login_url='user_login')
def update_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('view_blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'admin_pages/update_blog.html', {'form': form, 'blog': blog})

@login_required(login_url='user_login')
def delete_blog(request,id):
    places = Blog.objects.get(id=id)
    places.delete()
    return redirect('view_blogs')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

@csrf_exempt
def ckeditor_upload(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        file_extension = os.path.splitext(upload.name)[1].lower()
        
        # Check if the uploaded file is an image or a PDF
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            folder = 'images'
        elif file_extension == '.pdf':
            folder = 'pdfs'
        else:
            return JsonResponse({'uploaded': False, 'error': 'Unsupported file type.'})

        # Save the file in the appropriate folder
        file_name = default_storage.save(f'{folder}/{upload.name}', ContentFile(upload.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({
            'uploaded': True,
            'url': file_url
        })
    
    return JsonResponse({'uploaded': False, 'error': 'No file was uploaded.'})





# Client Reviews
@login_required(login_url='user_login')
def add_client_review(request):
    if request.method == 'POST':
        form = ClientReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_client_reviews') 
    else:
        form = ClientReviewForm()

    return render(request, 'admin_pages/add_client_review.html', {'form': form})


@login_required(login_url='user_login')
def view_client_reviews(request):
    client_reviews = ClientReview.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_client_reviews.html', {'client_reviews': client_reviews})


@login_required(login_url='user_login')
def update_client_review(request, id):
    client_reviews = get_object_or_404(ClientReview, id=id)
    if request.method == 'POST':
        form = ClientReviewForm(request.POST, request.FILES, instance=client_reviews)
        if form.is_valid():
            form.save()
            return redirect('view_client_reviews')
    else:
        form = ClientReviewForm(instance=client_reviews)
    return render(request, 'admin_pages/update_client_review.html', {'form': form, 'client_reviews': client_reviews})

    

@login_required(login_url='user_login')
def delete_client_review(request,id):
    client_reviews = ClientReview.objects.get(id=id)
    client_reviews.delete()
    return redirect('view_client_reviews')



# add folders
@login_required(login_url='user_login')
def add_folders(request):
    if request.method == 'POST':
        form = FolderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_images') 
    else:
        form = FolderForm()

    return render(request, 'admin_pages/add_folders.html', {'form': form})

@login_required(login_url='user_login')
def view_folders(request):
    folders = Folder.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_folders.html', {'folders': folders})

@login_required(login_url='user_login')
def update_folder(request, id):
    folder = get_object_or_404(Folder, id=id)
    if request.method == 'POST':
        form = FolderForm(request.POST, request.FILES, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('add_images')
    else:
        form = FolderForm(instance=folder)
    return render(request, 'admin_pages/update_folder.html', {'form': form, 'folder': folder})

@login_required(login_url='user_login')
def delete_folder(request,id):
    folder = Folder.objects.get(id=id)
    folder.delete()
    return redirect('view_folders')


# Add Images
@login_required(login_url='user_login')
def add_images(request):
    folders = Folder.objects.all()
    if request.method == 'POST':
        form = GalleryForm(request.POST)
        if form.is_valid():
            gallery = form.save()
            images = request.FILES.getlist('image')
            for image in images:
                GalleryImage.objects.create(gallery=gallery, image=image)
            return redirect('view_images')  # Redirect to wherever you want after successful upload
    else:
        form = GalleryForm()

    return render(request, 'admin_pages/add_images.html', {'form': form, 'folders': folders})

@login_required(login_url='user_login')
def view_images(request):
    galleries = Gallery.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_images.html', {'galleries': galleries})


@login_required(login_url='user_login')
def update_image(request, id):
    image = get_object_or_404(Gallery, id=id)
    folders = Folder.objects.all()
    
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            updated_image = form.save()

            # Handle image removal
            if 'remove_image' in request.POST:
                remove_image_ids = request.POST.getlist('remove_image')
                for image_id in remove_image_ids:
                    try:
                        image_to_remove = GalleryImage.objects.get(id=image_id)
                        image_to_remove.delete()
                    except GalleryImage.DoesNotExist:
                        pass

            # Save new images
            images = request.FILES.getlist('image')
            for img in images:
                GalleryImage.objects.create(gallery=updated_image, image=img)

            return redirect('view_images')
    else:
        form = GalleryForm(instance=image)

    return render(request, 'admin_pages/update_image.html', {'form': form, 'image': image, 'folders': folders})

@login_required(login_url='user_login')
def delete_image(request,id):
    image = Gallery.objects.get(id=id)
    image.delete()
    return redirect('view_images')



# Add Category
@login_required(login_url='user_login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_packages') 
    else:
        form = CategoryForm()

    return render(request, 'admin_pages/add_category.html', {'form': form})

@login_required(login_url='user_login')
def view_category(request):
    categories = Category.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_category.html', {'categories': categories})

@login_required(login_url='user_login')
def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('add_packages')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin_pages/update_category.html', {'category': category, 'category': category})

@login_required(login_url='user_login')
def delete_category(request,id):
    category = Category.objects.get(id=id)
    category.delete()   
    return redirect('view_category')


# PAckages
@login_required(login_url='user_login')
def add_packages(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_packages') 
    else:
        form = PackageForm()

    return render(request, 'admin_pages/add_packages.html', {'form': form, 'categories':categories})


@login_required(login_url='user_login')
def view_packages(request):
    packages = Package.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_packages.html', {'packages': packages})


@login_required(login_url='user_login')
def update_packages(request, id):
    package = get_object_or_404(Package, id=id)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect('view_packages')
    else:
        form = PackageForm(instance=package)
    return render(request, 'admin_pages/update_packages.html', {'form': form, 'package': package, 'categories':categories})

@login_required(login_url='user_login')
def delete_packages(request,id):
    packages = Package.objects.get(id=id)
    packages.delete()
    return redirect('view_packages')



    #  404 view\
def page_404(request, exception):
    return render(request, '404.html', status=404)