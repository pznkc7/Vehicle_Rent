from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from bookings.models import Booking
from vehicles.models import Vehicle

# Create your views here.

from django.utils import timezone
from datetime import timedelta

@login_required
def create_booking(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        service_type = request.POST.get("service_type")
        hours = request.POST.get("hours")
        days = request.POST.get("days")

        try:
            if service_type == 'hour':
                hours = int(hours) if hours else 0
                if hours > 10:
                    messages.error(request, "Maximum 10 hours allowed")
                    return redirect(request.path)
            elif service_type == 'day':
                days = int(days) if days else 0
                if days > 3:
                    messages.error(request, "Maximum 3 days allowed")
                    return redirect(request.path)
        except (ValueError, TypeError):
            messages.error(request, "Invalid hours or days provided")
            return redirect(request.path)

        price = (
            int(hours) * vehicle.price_per_hour
            if service_type == 'hour'
            else int(days) * vehicle.price_per_day
        )

        Booking.objects.create(
            user=request.user,
            vehicle=vehicle,
            service_type=service_type,
            hours=hours if service_type == 'hour' else None,
            days=days if service_type == 'day' else None,
            total_price=price,
            status='confirmed'
        )

        return redirect('my_bookings')

    return render(request, 'bookings/bookings.html', {'vehicle': vehicle})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def start_service(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user == booking.user or request.user == booking.vehicle.owner:
        if booking.status != 'active':
            booking.status = 'active'
            booking.save()

    return redirect('booking_detail', booking_id=booking.id)
