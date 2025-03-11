# # views.py
# from django.shortcuts import render, redirect
# from .models import Property

# # Display properties
# def property_list(request):
#     rent_properties = Property.objects.filter(property_type='rent')
#     buy_properties = Property.objects.filter(property_type='buy')
#     return render(request, 'properties/index.html', {'rent_properties': rent_properties, 'buy_properties': buy_properties})

# # Post new property
# def post_property(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         location = request.POST['location']
#         price = request.POST['price']
#         bedrooms = request.POST['bedrooms']
#         property_type = request.POST['property_type']
#         image = request.FILES['image']  # Get the uploaded image

#         Property.objects.create(
#             name=name,
#             location=location,
#             price=price,
#             bedrooms=bedrooms,
#             property_type=property_type,
#             image_url=image.name,
#         )
#         return redirect('property_list')
#     return render(request, 'properties/post_property.html')






# from django.shortcuts import render, redirect
# from .models import Property

# def post_property(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         location = request.POST['location']
#         price = request.POST['price']
#         bedrooms = request.POST['bedrooms']
#         property_type = request.POST['property_type']
#         reviews = request.POST.get('reviews', '')  # Use .get() to avoid KeyError
#         image = request.FILES['image']  # Get the uploaded image

#         # Save property to database (adjust image field accordingly)
#         property = Property(
#             name=name,
#             location=location,
#             price=price,
#             bedrooms=bedrooms,
#             property_type=property_type,
#             image_url=image.name,  # or save the file properly using Django's FileField
#         )
#         property.save()

#         return redirect('property_list')  # Redirect to homepage or property list

#     return render(request, 'post_property.html')






from django.shortcuts import render, redirect
from .models import Property

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

        Property.objects.create(
            name=name,
            location=location,
            price=price,
            bedrooms=bedrooms,
            property_type=property_type,
            image=image  # Make sure this matches your model field
        )

        return redirect('property_list')

    return render(request, 'properties/post_property.html')





