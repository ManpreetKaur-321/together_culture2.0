from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Event
from users.models import User

User = get_user_model()

class EventModelTest(TestCase):
    def setUp(self):
        self.event_data = {
            'title': 'Test Event',
            'description': 'Test event description',
            'date': timezone.now() + timezone.timedelta(days=7),
            'location': 'Test Location',
            'is_digital': False,
            'is_active': True
        }
    
    def test_event_creation(self):
        """Test event creation"""
        event = Event.objects.create(**self.event_data)
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.description, 'Test event description')
        self.assertFalse(event.is_digital)
        self.assertTrue(event.is_active)
    
    def test_digital_event_creation(self):
        """Test digital event creation"""
        digital_event_data = self.event_data.copy()
        digital_event_data.update({
            'title': 'Digital Content',
            'is_digital': True,
            'digital_content_url': 'https://example.com/content'
        })
        
        event = Event.objects.create(**digital_event_data)
        self.assertEqual(event.title, 'Digital Content')
        self.assertTrue(event.is_digital)
        self.assertEqual(event.digital_content_url, 'https://example.com/content')
    
    def test_event_str(self):
        """Test event string representation"""
        event = Event.objects.create(**self.event_data)
        self.assertEqual(str(event), 'Test Event')
    
    def test_event_ordering(self):
        """Test event ordering by date"""
        event1 = Event.objects.create(
            title='Event 1',
            description='First event',
            date=timezone.now() + timezone.timedelta(days=1),
            location='Location 1',
            is_digital=False,
            is_active=True
        )
        event2 = Event.objects.create(
            title='Event 2',
            description='Second event',
            date=timezone.now() + timezone.timedelta(days=2),
            location='Location 2',
            is_digital=False,
            is_active=True
        )
        
        events = Event.objects.filter(is_digital=False, is_active=True).order_by('date')
        self.assertEqual(events[0], event1)
        self.assertEqual(events[1], event2)

class DigitalContentFilterTest(TestCase):
    def setUp(self):
        # Create regular events
        self.regular_event = Event.objects.create(
            title='Regular Event',
            description='Regular event description',
            date=timezone.now() + timezone.timedelta(days=7),
            location='Test Location',
            is_digital=False,
            is_active=True
        )
        
        # Create digital events
        self.digital_event = Event.objects.create(
            title='Digital Content',
            description='Digital content description',
            date=timezone.now(),
            location='Online',
            is_digital=True,
            is_active=True,
            digital_content_url='https://example.com/content'
        )
    
    def test_regular_events_filter(self):
        """Test filtering for regular events only"""
        regular_events = Event.objects.filter(is_digital=False, is_active=True)
        self.assertEqual(len(regular_events), 1)
        self.assertEqual(regular_events[0], self.regular_event)
    
    def test_digital_events_filter(self):
        """Test filtering for digital events only"""
        digital_events = Event.objects.filter(is_digital=True, is_active=True)
        self.assertEqual(len(digital_events), 1)
        self.assertEqual(digital_events[0], self.digital_event)
    
    def test_all_active_events(self):
        """Test getting all active events"""
        active_events = Event.objects.filter(is_active=True)
        self.assertEqual(len(active_events), 2)
        self.assertIn(self.regular_event, active_events)
        self.assertIn(self.digital_event, active_events)
