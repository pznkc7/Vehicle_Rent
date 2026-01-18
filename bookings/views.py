from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Booking
from vehicles.models import Vehicle


@login_required
def create_booking(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        service_type = request.POST.get("service_type")
        booking_date = request.POST.get("booking_date")
        start_time = request.POST.get("start_time")
        hours = request.POST.get("hours")
        days = request.POST.get("days")

        if not booking_date or not start_time or not service_type:
            messages.error(request, "Please fill all required fields.")
            return redirect(request.path)

        try:
            booking_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time, "%H:%M").time()
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return redirect(request.path)

        hours = int(hours) if hours else None
        days = int(days) if days else None

        if service_type == 'hour':
            if not hours or hours < 1 or hours > 10:
                messages.error(request, "Hourly booking must be between 1–10 hours.")
                return redirect(request.path)

            total_price = hours * vehicle.price_per_hour

        elif service_type == 'day':
            if not days or days < 1 or days > 3:
                messages.error(request, "Daily booking must be between 1–3 days.")
                return redirect(request.path)

            total_price = days * vehicle.price_per_day

        else:
            messages.error(request, "Invalid service type.")
            return redirect(request.path)

        Booking.objects.create(
            user=request.user,
            vehicle=vehicle,
            service_type=service_type,
            booking_date=booking_date,
            start_time=start_time,
            hours=hours if service_type == 'hour' else None,
            days=days if service_type == 'day' else None,
            total_price=total_price,
            status='confirmed'
        )

        messages.success(request, "Booking created successfully.")
        return redirect('my_bookings')

    return render(request, 'bookings/bookings.html', {'vehicle': vehicle})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def start_service(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user not in [booking.user, booking.vehicle.owner]:
        messages.error(request, "Unauthorized action.")
        return redirect('my_bookings')

    if booking.status != 'active':
        start_datetime = datetime.combine(
            booking.booking_date,
            booking.start_time
        )

        start_datetime = timezone.make_aware(start_datetime)

        if booking.service_type == 'hour':
            booking.expected_end_at = start_datetime + timedelta(hours=booking.hours)
        else:
            booking.expected_end_at = start_datetime + timedelta(days=booking.days)

        booking.status = 'active'
        booking.save()
        messages.success(request, "Service started.")

    return redirect('my_bookings')
