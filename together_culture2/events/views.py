from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from bookings.models import Booking
from members.models import MemberProfile

# Create your views here.

@login_required
def event_list(request):
    # Exclude digital content events - only show regular events
    events = Event.objects.filter(is_digital=False).order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    member_profile = MemberProfile.objects.get(user=request.user)
    # Check if already booked
    if Booking.objects.filter(member=member_profile, event=event).exists():
        messages.warning(request, f'You have already requested to book "{event.title}".')
    else:
        # Create booking with pending approval
        Booking.objects.create(member=member_profile, event=event, is_approved=False)
        messages.success(request, f'Booking request for "{event.title}" submitted. Waiting for admin approval.')
    return redirect('event_list')
