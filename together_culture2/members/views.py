from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MemberProfile
from bookings.models import Booking
from events.models import Event

# Create your views here.

@login_required
def dashboard(request):
    profile, created = MemberProfile.objects.get_or_create(user=request.user)
    approved_bookings = Booking.objects.filter(member=profile, is_approved=True).select_related('event')
    pending_bookings = Booking.objects.filter(member=profile, is_approved=False).select_related('event')
    
    # Get events that are not booked (neither approved nor pending)
    booked_event_ids = Booking.objects.filter(member=profile).values_list('event_id', flat=True)
    available_events = Event.objects.exclude(id__in=booked_event_ids).order_by('date')
    
    return render(request, 'members/dashboard.html', {
        'profile': profile,
        'approved_bookings': approved_bookings,
        'pending_bookings': pending_bookings,
        'available_events': available_events,
    })

@login_required
def cancel_booking(request, booking_id):
    profile = MemberProfile.objects.get(user=request.user)
    booking = Booking.objects.filter(id=booking_id, member=profile).first()
    if booking:
        booking.delete()
    return redirect('dashboard')
