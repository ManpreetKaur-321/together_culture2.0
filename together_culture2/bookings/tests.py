from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Booking
from events.models import Event
from members.models import MemberProfile
from users.models import User

User = get_user_model()

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testmember',
            email='member@example.com',
            password='testpass123',
            role=User.MEMBER
        )
        # MemberProfile should be created automatically via signal
        self.member_profile = MemberProfile.objects.get(user=self.user)
        self.member_profile.interests = 'caring'
        self.member_profile.status = 'authorized'
        self.member_profile.save()
        
        self.event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            date=timezone.now() + timezone.timedelta(days=7),
            location='Test Location',
            is_digital=False,
            is_active=True
        )
    
    def test_booking_creation(self):
        """Test booking creation"""
        booking = Booking.objects.create(
            member=self.member_profile,
            event=self.event,
            is_approved=False
        )
        self.assertEqual(booking.member, self.member_profile)
        self.assertEqual(booking.event, self.event)
        self.assertFalse(booking.is_approved)
        self.assertIsNotNone(booking.booked_at)
    
    def test_booking_str(self):
        """Test booking string representation"""
        booking = Booking.objects.create(
            member=self.member_profile,
            event=self.event,
            is_approved=False
        )
        self.assertEqual(str(booking), 'testmember booked Test Event')
    
    def test_booking_approval(self):
        """Test booking approval"""
        booking = Booking.objects.create(
            member=self.member_profile,
            event=self.event,
            is_approved=False
        )
        
        booking.is_approved = True
        booking.save()
        
        self.assertTrue(booking.is_approved)
    
    def test_booking_ordering(self):
        """Test booking ordering by booked_at"""
        booking1 = Booking.objects.create(
            member=self.member_profile,
            event=self.event,
            is_approved=False
        )
        
        # Create another event and booking
        event2 = Event.objects.create(
            title='Test Event 2',
            description='Test event 2 description',
            date=timezone.now() + timezone.timedelta(days=8),
            location='Test Location 2',
            is_digital=False,
            is_active=True
        )
        
        booking2 = Booking.objects.create(
            member=self.member_profile,
            event=event2,
            is_approved=False
        )
        
        bookings = Booking.objects.filter(member=self.member_profile).order_by('-booked_at')
        self.assertEqual(bookings[0], booking2)  # Most recent first
        self.assertEqual(bookings[1], booking1)
