from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import MemberProfile, MembershipType, Benefit, MemberBenefitUsage
from events.models import Event
from bookings.models import Booking
from users.models import User

User = get_user_model()

class MemberProfileTest(TestCase):
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
    
    def test_member_profile_creation(self):
        """Test member profile creation"""
        self.assertEqual(self.member_profile.user.username, 'testmember')
        self.assertEqual(self.member_profile.interests, 'caring')
        self.assertEqual(self.member_profile.status, 'authorized')
    
    def test_member_profile_str(self):
        """Test member profile string representation"""
        self.assertEqual(str(self.member_profile), 'Profile: testmember')

class BenefitModelTest(TestCase):
    def setUp(self):
        self.benefit = Benefit.objects.create(
            name='Test Benefit',
            description='Test benefit description',
            benefit_type='event_access'
        )
    
    def test_benefit_creation(self):
        """Test benefit creation"""
        self.assertEqual(self.benefit.name, 'Test Benefit')
        self.assertEqual(self.benefit.description, 'Test benefit description')
        self.assertEqual(self.benefit.benefit_type, 'event_access')
    
    def test_benefit_str(self):
        """Test benefit string representation"""
        self.assertEqual(str(self.benefit), 'Test Benefit')

class MembershipTypeTest(TestCase):
    def setUp(self):
        self.membership_type = MembershipType.objects.create(
            name='Test Membership',
            description='Test membership description',
            membership_category='test'
        )
    
    def test_membership_type_creation(self):
        """Test membership type creation"""
        self.assertEqual(self.membership_type.name, 'Test Membership')
        self.assertEqual(self.membership_type.description, 'Test membership description')
        self.assertEqual(self.membership_type.membership_category, 'test')
    
    def test_membership_type_str(self):
        """Test membership type string representation"""
        self.assertEqual(str(self.membership_type), 'Test Membership')
