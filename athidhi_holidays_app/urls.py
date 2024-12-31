from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('', views.index, name= 'index'),
        path('about', views.about, name= 'about'),
        path('destinations', views.destinations, name= 'destinations'),
        path('destination/<int:id>/', views.destination_details, name= 'destination_details'),
        path('packages', views.packages, name= 'packages'),
        path('package/<int:id>/', views.package_details, name= 'package_details'),
        path('blogs/', views.blogs, name='blogs'),
        path('blogs/<int:blog_id>/', views.blog_details, name='blog_details'),
        path('gallery', views.gallery, name= 'gallery'),
        path('contact', views.contact, name= 'contact'),
        path('booking', views.booking, name= 'booking'),
        path('get_related_packages/', views.get_related_packages, name='get_related_packages'),
        path('get_tourist_places/', views.get_tourist_places, name='get_tourist_places'),

        
        # Admin Login
        path('login',views.user_login,name='user_login'),
        path('logout_user', views.logout_user, name='logout_user'),

        # admin dashboard
        path('dashboard',views.dashboard,name='dashboard'),

        # Contact us
        path('contact_view',views.contact_view,name='contact_view'),
        path('delete_contact/<int:id>/',views.delete_contact,name='delete_contact'),

        
        # Booking
        path('booking_view',views.booking_view,name='booking_view'),
        path('delete_booking/<int:id>/',views.delete_booking,name='delete_booking'),

        # Add District
        path('add_district', views.add_district, name='add_district'),
        path('view_districts',views.view_districts,name='view_districts'),
        path('update_district/<int:id>/',views.update_district,name='update_district'),
        path('delete_district/<int:id>/',views.delete_district,name='delete_district'),

         # Destination
        path('add_destinations', views.add_destinations, name='add_destinations'),
        path('view_destinations',views.view_destinations,name='view_destinations'),
        path('update_destination/<int:id>/',views.update_destination,name='update_destination'),
        path('delete_destination/<int:id>/',views.delete_destination,name='delete_destination'),

        # blogs
        path('add_blog', views.add_blog, name='add_blog'),
        path('view_blogs',views.view_blogs,name='view_blogs'),
        path('update_blog/<int:id>/',views.update_blog,name='update_blog'),
        path('delete_blog/<int:id>/',views.delete_blog,name='delete_blog'),

        path('ckeditor_upload/', views.ckeditor_upload, name='ckeditor_upload'),

        # client reviews
        path('add_client_review',views.add_client_review,name='add_client_review'),
        path('view_client_reviews',views.view_client_reviews,name='view_client_reviews'),
        path('update_client_review/<int:id>/',views.update_client_review,name='update_client_review'),
        path('delete_client_review/<int:id>/',views.delete_client_review,name='delete_client_review'),

        # Add Folders
        path('add_folders', views.add_folders, name='add_folders'),
        path('view_folders',views.view_folders,name='view_folders'),
        path('update_folder/<int:id>/',views.update_folder,name='update_folder'),
        path('delete_folder/<int:id>/',views.delete_folder,name='delete_folder'),

        # Add Images
        path('add_images', views.add_images, name='add_images'),
        path('view_images',views.view_images,name='view_images'),
        path('update_image/<int:id>/',views.update_image,name='update_image'),
        path('delete_image/<int:id>/',views.delete_image,name='delete_image'),

             # Add Category
        path('add_category', views.add_category, name='add_category'),
        path('view_category',views.view_category,name='view_category'),
        path('update_category/<int:id>/',views.update_category,name='update_category'),
        path('delete_category/<int:id>/',views.delete_category,name='delete_category'),

         # Packages
        path('add_packages', views.add_packages, name='add_packages'),
        path('view_packages',views.view_packages,name='view_packages'),
        path('update_packages/<int:id>/',views.update_packages,name='update_packages'),
        path('delete_packages/<int:id>/',views.delete_packages,name='delete_packages'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'athidhi_holidays_app.views.page_404'