from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


# Create your views here.


# --------------------------------VEHICLES VIEW---------------------------------

from vehicles.models import Vehicle
from django.shortcuts import  get_object_or_404
from bookings.models import Booking



def vehicles(request):
    vehicles = Vehicle.objects.filter(status='approved', is_available=True)

    # Get filters from GET request
    search_query = request.GET.get('q', '')
    vehicle_type = request.GET.get('type', '')
    max_price = request.GET.get('price', '')

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

    context = {
        'vehicles': vehicles,
        'request': request
    }
    return render(request, 'vehicles/vehicles.html', context)

def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    active_booking = None
    if request.user.is_authenticated:
        active_booking = Booking.objects.filter(
            vehicle=vehicle,
            status='active'
        ).first()
    
    context = {
        'vehicle': vehicle,
        'active_booking': active_booking,
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



    