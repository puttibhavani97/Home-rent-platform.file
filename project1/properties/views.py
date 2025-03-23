from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Property, Contact
from django.contrib.auth.decorators import login_required
from .models import Property, Booking
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from datetime import datetime  # ✅ Import datetime
from django.shortcuts import render
import json
from .models import Payment
from django.views.decorators.csrf import csrf_exempt


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
    



# def book_now(request, property_id):
#     property_obj = get_object_or_404(Property, id=property_id)
    
#     if request.method == 'POST':
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
        
#         try:
#             booking = Booking.objects.create(
#                 property=property_obj,
#                 user=request.user,
#                 start_date=start_date,
#                 end_date=end_date,
#                 status='pending'
#             )
#             messages.success(request, 'Property booked successfully!')
#             return redirect('booking_confirmation')
        
#         except Exception as e:
#             messages.error(request, f'Error booking property: {str(e)}')
#             return redirect('property_detail', property_id=property_id)
    
#     return render(request, 'properties/book_now.html', {'property': property_obj})


# @login_required(login_url='/signin/')
# def book_now(request, property_id):
#     property_obj = get_object_or_404(Property, id=property_id)

#     if request.method == 'POST':
#         # Form nunchi booking details techadam
#         check_in_date = request.POST.get('check_in_date')  # Booking start date
#         check_out_date = request.POST.get('check_out_date')  # Booking end date

#         # Booking create cheyyadam
#         booking = Booking.objects.create(
#             user=request.user,  # Logged-in user
#             property=property_obj,  # Property object
#             check_in_date=check_in_date,
#             check_out_date=check_out_date,
        
        
#         )

#         # Booking ayyaka agreement page ki redirect cheyyadam
#         return redirect('agreement', booking_id=booking.id)

#     return render(request, 'properties/book_now.html', {'property': property_obj})




@login_required(login_url='/signin/')
def book_now(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        # Form nunchi booking details techadam
        check_in_date = request.POST.get('check_in_date')  # Booking start date
        check_out_date = request.POST.get('check_out_date')  # Booking end date
        
        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Invalid date format", status=400)

        # Check in date check cheyyadam
        if check_in_date >= check_out_date:
            return HttpResponse("Check-out date must be after check-in date.", status=400)

        # Booking create cheyyadam
        booking = Booking.objects.create(
            user=request.user,  # Logged-in user
            property=property_obj,  # Property object
            check_in_date=check_in_date,
            check_out_date=check_out_date,
           
        )

        # Booking ayyaka agreement page ki redirect cheyyadam
        return redirect('agreement', booking_id=booking.id)

    return render(request, 'properties/book_now.html', {'property': property_obj})



def agreement(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'properties/agreement.html', {'booking': booking})

def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)  # Get booking details
    return render(request, 'properties/payment.html', {'booking': booking})

# @login_required
# def process_payment(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)

#             # Retrieve user from the request
#             user = request.user

#             # Extract payment details
#             card_name = data.get("card_name")
#             card_number = data.get("card_number")
#             expiry_date = data.get("expiry_date")
#             cvv = data.get("cvv")
#             amount = data.get("amount")

#             # Save payment details to database
#             payment = Payment.objects.create(
#                 user=user,
#                 card_name=card_name,
#                 card_number=card_number,
#                 expiry_date=expiry_date,
#                 cvv=cvv,
#                 amount=amount
#             )

#             return JsonResponse({"status": "success", "message": "Payment successful!", "payment_id": payment.id})

#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)})
    
#     return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)



@login_required  # Only logged-in users can make payments
@csrf_exempt  # Remove this later and use CSRF token
def process_payment(request, booking_id):
    if request.method == "POST":
        try:
            # 🔍 Print raw request body for debugging
            print("🔍 Raw Request Body:", request.body)

            # Decode and parse JSON data
            data = json.loads(request.body.decode("utf-8"))

            # 🔍 Print parsed JSON data
            print("✅ Parsed JSON Data:", data)

            # Extract fields
            card_name = data.get("card_name")
            card_number = data.get("card_number")
            expiry_date = data.get("expiry_date")
            cvv = data.get("cvv")
            amount = data.get("amount")

            # Validate required fields
            if not all([card_name, card_number, expiry_date, cvv, amount]):
                return JsonResponse({"status": "error", "message": "Missing required fields"}, status=400)

            # Payment success response
            return JsonResponse({
                "status": "success",
                "message": f"Payment for booking {booking_id} processed successfully!"
            })

        except json.JSONDecodeError:
            print("❌ JSON Decode Error: Invalid JSON format!")
            return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def download_invoice(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{booking.id}.pdf"'
    
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Invoice for Booking ID: {booking.id}")
    p.drawString(100, 780, f"Tenant: {booking.user.username}")
    p.drawString(100, 760, f"Property: {booking.property.name}")  # Corrected field
    p.drawString(100, 720, "Thank you for choosing House Rent Platform!")
    p.showPage()
    p.save()
    return response

def booking_confirmation(request):
    return render(request, 'properties/booking_confirmation.html')  # Correct template name