from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


# Create your views here.


# --------------------------------VEHICLES VIEW---------------------------------

from vehicles.models import Vehicle
from django.shortcuts import  get_object_or_404
from math import radians, cos, sin, asin, sqrt

# Haversine formula to calculate distance in km
def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6371 * c
    return km

def vehicles(request):
    vehicles = Vehicle.objects.filter(status='approved', is_available=True)

    # Get filters from GET request
    search_query = request.GET.get('q', '')
    vehicle_type = request.GET.get('type', '')
    max_price = request.GET.get('price', '')
    user_lat = request.GET.get('latitude')
    user_lng = request.GET.get('longitude')
    max_distance = float(request.GET.get('distance', 10))  # default 10 km radius

    # Filter by search
    if search_query:
        vehicles = vehicles.filter(vehicle_name__icontains=search_query)

    # Filter by type
    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type)

    # Filter by price
    if max_price:
        try:
            price = float(max_price)
            vehicles = vehicles.filter(price_per_day__lte=price)
        except:
            pass

    # Filter by nearby location
    if user_lat and user_lng:
        user_lat = float(user_lat)
        user_lng = float(user_lng)
        nearby_vehicles = []
        for v in vehicles:
            if v.latitude and v.longitude:
                distance = haversine(user_lat, user_lng, v.latitude, v.longitude)
                if distance <= max_distance:
                    nearby_vehicles.append(v.id)
        vehicles = vehicles.filter(id__in=nearby_vehicles)

    context = {
        'vehicles': vehicles,
        'request': request
    }
    return render(request, 'vehicles/vehicles.html', context)

def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    context = {
        'vehicle': vehicle,
        'latitude': vehicle.latitude,    # Pass latitude
        'longitude': vehicle.longitude,  # Pass longitude
    }
    
    return render(request, 'vehicles/vehicles_detail.html', context)


#--------------------------------APPLY VEHICLE VIEW---------------------------------
from .forms import VehicleApplicationForm

@login_required
def apply_vehicle(request):
    if request.method == 'POST':
        form = VehicleApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.status = 'pending'
            vehicle.is_available = False
            vehicle.save()
            return redirect('vehicle_application_success')
        else  :
            print(form.errors)  # For debugging purposes
    else:
        form = VehicleApplicationForm()

    return render(request, 'vehicles/apply_vehicle.html', {
        'form': form
    })

@login_required
def my_vehicle_applications(request):
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(
        request,
        'vehicles/my_vehicle_applications.html',
        {'vehicles': vehicles}
    )


@login_required
def vehicle_application_success(request):
    return render(request, 'vehicles/application_success.html')

# ----------------------BOOKING VIEW--------------------------------

from datetime import date
from django.shortcuts import  get_object_or_404
from vehicles.models import Booking , Vehicle

@login_required
def book_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')

        conflict = Booking.objects.filter(
            vehicle=vehicle,
            start_date__lte=end,
            end_date__gte=start
        ).exists()

        if conflict:
            return render(request, 'booking.html', {
                'vehicle': vehicle,
                'error': 'Vehicle not available for selected dates'
            })

        Booking.objects.create(
            user=request.user,
            vehicle=vehicle,
            start_date=start,
            end_date=end
        )

        return redirect('my_bookings')

    return render(request, 'vehicles/booking.html', {'vehicle': vehicle})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'vehicles/my_bookings.html', {'bookings': bookings})


    