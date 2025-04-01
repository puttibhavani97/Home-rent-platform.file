from django.urls import path
from . import views

from django.urls import path
# from .views import user_login, user_signup, user_logout
from .views import property_list, post_property, index, login_view, signup_view, logout_view, get_contact_details,payment, process_payment, about_us, redirect_about, index, download_invoice



urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('post-property/', views.post_property, name='post_property'),

    # Authentication URLs
    path('index/', index, name='index'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),

    path('contact/<int:property_id>/', get_contact_details, name='get_contact_details'),

    path('book_now/<int:property_id>/', views.book_now, name='book_now'),
    path('agreement/<int:booking_id>/', views.agreement, name='agreement'),
    path('download_invoice/<int:payment_id>/', download_invoice, name='download_invoice'),
    path('process_payment/<int:booking_id>/', process_payment, name='process_payment'),
    path('download_invoice/<int:payment_id>/', download_invoice, name='download_invoice'), 
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),  # Change name here

    path("aboutus.html", redirect_about),  # Redirect old URL
    path("about-us/", about_us, name="about_us"),

    path('payment/<int:booking_id>/', payment, name='payment'),
    path("", index, name="index"),  # Home Page

    path('investment-advice/', views.investment_advice, name='investment_advice'),

    
]


    


