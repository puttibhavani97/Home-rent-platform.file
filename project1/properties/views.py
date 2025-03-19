from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Property, Contact
from .models import Property, Booking


# from django.shortcuts import render

# post-property code

def property_list(request):
    rent_properties = Property.objects.filter(property_type='Rent')
    buy_properties = Property.objects.filter(property_type='Buy')
    return render(request, 'properties/index.html', {
        'rent_properties': rent_properties,
        'buy_properties': buy_properties
    })

def post_property(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        price = request.POST.get('price')
        bedrooms = request.POST.get('bedrooms')
        property_type = request.POST.get('property_type')
        image = request.FILES.get('image')

        contact_name = request.POST.get('contact_name')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')

        # property_obj = Property.objects.create(
        #     name=name,
        #     location=location,
        #     price=price,
        #     bedrooms=bedrooms,
        #     property_type=property_type,
        #     image=image
        # )

        property_instance =Property.objects.create(
            name=name,
            location=location,
            price=price,
            bedrooms=bedrooms,
            property_type=property_type,
            image=image  # Make sure this matches your model field
        )

        Contact.objects.create(
            property=property_instance,
            name=contact_name,
            phone=contact_phone,
            email=contact_email
        )


        return redirect('property_list')

    return render(request, 'properties/post_property.html')


# sign-in and sign-up code

def index(request):
    return render(request, 'properties/index.html')  # Load the main page

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)  # Auto login after sign-up
        return redirect('index')  # Redirect to main page

    return render(request, 'accounts/signin.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to main page
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'accounts/signin.html')


def logout_view(request):
    logout(request)
    return redirect('index')

# Fetch contact details
# def get_contact_details(request, property_id):
#     property_instance = get_object_or_404(Property, id=property_id)
#     contact = Contact.objects.filter(property=property_instance).first()
    
#     if contact:
#         return JsonResponse({
#             'success': True,
#             'name': contact.name,
#             'phone': contact.phone,
#             'email': contact.email
#         })
#     else:
#         return JsonResponse({'success': False})


def get_contact_details(request, property_id):
    try:
        contact = Contact.objects.get(property_id=property_id)
        return JsonResponse({
            'success': True,
            'name': contact.name,
            'phone': contact.phone,
            'email': contact.email
        })
    except contact.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'contact details not found'})
    



def book_now(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        try:
            booking = Booking.objects.create(
                property=property_obj,
                user=request.user,
                start_date=start_date,
                end_date=end_date,
                status='pending'
            )
            messages.success(request, 'Property booked successfully!')
            return redirect('booking_confirmation')
        
        except Exception as e:
            messages.error(request, f'Error booking property: {str(e)}')
            return redirect('property_detail', property_id=property_id)
    
    return render(request, 'properties/book_now.html', {'property': property_obj})
