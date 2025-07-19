from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from users.models import User
from members.models import MemberProfile
from events.models import Event
from bookings.models import Booking

def is_admin(user):
    return user.is_authenticated and user.role == User.ADMIN

def test_view(request):
    return HttpResponse("Dashboard app is working!")

def debug_admin_dashboard(request):
    """Debug version to check user role and template"""
    if not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    
    user_info = f"""
    <h2>User Debug Info</h2>
    <p>Username: {request.user.username}</p>
    <p>Role: {request.user.role}</p>
    <p>Is Admin: {request.user.role == User.ADMIN}</p>
    <p>Is Authenticated: {request.user.is_authenticated}</p>
    """
    
    if request.user.role == User.ADMIN:
        # Try to render the template
        try:
            context = {
                'total_members': MemberProfile.objects.count(),
                'total_events': Event.objects.count(),
                'pending_bookings': Booking.objects.filter(is_approved=False).count(),
                'approved_bookings': Booking.objects.filter(is_approved=True).count(),
                'recent_bookings': [],
                'recent_members': [],
                'interest_stats': [],
                'events_by_month': [],
                'pending_approvals': [],
            }
            return render(request, 'dashboard/admin_dashboard.html', context)
        except Exception as e:
            return HttpResponse(f"Template error: {str(e)}")
    else:
        return HttpResponse(f"Not admin. Your role is: {request.user.role}")

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get statistics
    total_members = MemberProfile.objects.count()
    total_events = Event.objects.count()
    pending_bookings = Booking.objects.filter(is_approved=False).count()
    approved_bookings = Booking.objects.filter(is_approved=True).count()
    
    # Recent activities
    recent_bookings = Booking.objects.select_related('member__user', 'event').order_by('-booked_at')[:10]
    recent_members = MemberProfile.objects.select_related('user').order_by('-user__date_joined')[:5]
    
    # Member statistics by interest
    interest_stats = MemberProfile.objects.values('interests').annotate(count=Count('id')).order_by('-count')
    
    # Events by month (last 6 months)
    six_months_ago = timezone.now() - timedelta(days=180)
    events_by_month = Event.objects.filter(date__gte=six_months_ago).extra(
        select={'month': "EXTRACT(month FROM date)"}
    ).values('month').annotate(count=Count('id'))
    
    # Pending approvals for quick action
    pending_approvals = Booking.objects.filter(is_approved=False).select_related('member__user', 'event')[:5]
    
    context = {
        'total_members': total_members,
        'total_events': total_events,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'recent_bookings': recent_bookings,
        'recent_members': recent_members,
        'interest_stats': interest_stats,
        'events_by_month': events_by_month,
        'pending_approvals': pending_approvals,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)
