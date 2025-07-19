from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import MemberProfile, MembershipType, Benefit, MemberBenefitUsage
from bookings.models import Booking
from events.models import Event
from users.models import User

# Create your views here.

@login_required
def dashboard(request):
    if request.user.role != User.MEMBER:
        return redirect('admin_dashboard')
    
    member = request.user.memberprofile
    bookings = Booking.objects.filter(member=member).order_by('-booked_at')
    
    # Get available events that are not booked
    booked_event_ids = Booking.objects.filter(member=member).values_list('event_id', flat=True)
    available_events = Event.objects.exclude(id__in=booked_event_ids).filter(is_active=True).order_by('date')
    
    context = {
        'member': member,
        'bookings': bookings,
        'approved_bookings': bookings.filter(is_approved=True),
        'pending_bookings': bookings.filter(is_approved=False),
        'available_events': available_events,
    }
    return render(request, 'members/dashboard.html', context)

@login_required
def cancel_booking(request, booking_id):
    if request.user.role != User.MEMBER:
        return redirect('admin_dashboard')
    
    booking = get_object_or_404(Booking, id=booking_id, member=request.user.memberprofile)
    booking.delete()
    messages.success(request, 'Booking cancelled successfully.')
    return redirect('dashboard')

@login_required
def profile(request):
    """Member profile page where they can update their information"""
    if request.user.role != User.MEMBER:
        messages.error(request, 'Access denied. Member privileges required.')
        return redirect('dashboard')
    
    member = request.user.memberprofile
    membership_types = MembershipType.objects.all()
    
    if request.method == 'POST':
        # Update member profile
        member.interests = request.POST.get('interests', member.interests)
        member.bio = request.POST.get('bio', member.bio)
        member.phone = request.POST.get('phone', member.phone)
        member.address = request.POST.get('address', member.address)
        member.orientation_info = request.POST.get('orientation_info', member.orientation_info)
        
        # Update membership type if provided
        membership_type_id = request.POST.get('membership_type')
        if membership_type_id:
            try:
                membership_type = MembershipType.objects.get(id=membership_type_id)
                member.membership_type = membership_type
            except MembershipType.DoesNotExist:
                pass
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            member.profile_picture = request.FILES['profile_picture']
        
        member.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'member': member,
        'membership_types': membership_types,
    }
    return render(request, 'members/profile.html', context)

@login_required
def benefits_dashboard(request):
    """Member benefits dashboard showing used and unused benefits"""
    if request.user.role != User.MEMBER:
        messages.error(request, 'Access denied. Member privileges required.')
        return redirect('dashboard')
    
    member = request.user.memberprofile
    available_benefits = member.get_available_benefits()
    used_benefits = member.get_used_benefits()
    unused_benefits = member.get_unused_benefits()
    
    if request.method == 'POST':
        benefit_id = request.POST.get('benefit_id')
        if benefit_id:
            try:
                benefit = Benefit.objects.get(id=benefit_id)
                if benefit in available_benefits:
                    MemberBenefitUsage.objects.create(member=member, benefit=benefit)
                    messages.success(request, f'Benefit "{benefit.name}" marked as used.')
                    return redirect('benefits_dashboard')
            except Benefit.DoesNotExist:
                messages.error(request, 'Benefit not found.')
    
    context = {
        'member': member,
        'available_benefits': available_benefits,
        'used_benefits': used_benefits,
        'unused_benefits': unused_benefits,
    }
    return render(request, 'members/benefits_dashboard.html', context)

@login_required
def digital_content(request):
    """Digital content modules for members"""
    if request.user.role != User.MEMBER:
        messages.error(request, 'Access denied. Member privileges required.')
        return redirect('dashboard')
    
    member = request.user.memberprofile
    digital_events = Event.objects.filter(
        is_digital=True,
        is_active=True
    ).order_by('-date')
    
    context = {
        'member': member,
        'digital_events': digital_events,
    }
    return render(request, 'members/digital_content.html', context)

@login_required
def manage_members(request):
    """Admin view to manage member profiles"""
    if request.user.role != User.ADMIN:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    members = MemberProfile.objects.all().order_by('-user__date_joined')
    membership_types = MembershipType.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        member_id = request.POST.get('member_id')
        
        if action == 'authorize' and member_id:
            member = get_object_or_404(MemberProfile, id=member_id)
            member.status = 'authorized'
            member.authorized_at = timezone.now()
            member.authorized_by = request.user
            member.save()
            messages.success(request, f'Member {member.user.username} has been authorized.')
            
        elif action == 'deauthorize' and member_id:
            member = get_object_or_404(MemberProfile, id=member_id)
            member.status = 'pending'
            member.authorized_at = None
            member.authorized_by = None
            member.save()
            messages.success(request, f'Member {member.user.username} has been deauthorized.')
            
        elif action == 'update_interests' and member_id:
            member = get_object_or_404(MemberProfile, id=member_id)
            member.interests = request.POST.get('interests', member.interests)
            member.orientation_info = request.POST.get('orientation_info', member.orientation_info)
            member.membership_type_id = request.POST.get('membership_type') or None
            member.save()
            messages.success(request, f'Member {member.user.username} profile updated.')
    
    context = {
        'members': members,
        'membership_types': membership_types,
    }
    return render(request, 'members/manage_members.html', context)

@login_required
def member_detail(request, member_id):
    """Admin view to see detailed member information"""
    if request.user.role != User.ADMIN:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    member = get_object_or_404(MemberProfile, id=member_id)
    bookings = Booking.objects.filter(member=member).order_by('-booked_at')
    
    context = {
        'member': member,
        'bookings': bookings,
        'total_bookings': bookings.count(),
        'approved_bookings': bookings.filter(is_approved=True).count(),
        'pending_bookings': bookings.filter(is_approved=False).count(),
    }
    return render(request, 'members/member_detail.html', context)
