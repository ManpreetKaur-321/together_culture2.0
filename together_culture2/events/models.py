from django.db import models
from django.contrib.auth import get_user_model
from tags.models import Tag

User = get_user_model()

class Event(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('meetup', 'Meetup'),
        ('training', 'Training'),
        ('digital_content', 'Digital Content'),
        ('orientation', 'Orientation'),
        ('networking', 'Networking'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField(default=50)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='meetup')
    is_digital = models.BooleanField(default=False, help_text='Is this a digital content module?')
    digital_content_url = models.URLField(blank=True, null=True, help_text='URL for digital content')
    tags = models.ManyToManyField(Tag, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.title
    
    @property
    def available_spots(self):
        from bookings.models import Booking
        booked_count = Booking.objects.filter(event=self, is_approved=True).count()
        return max(0, self.capacity - booked_count)
    
    @property
    def is_full(self):
        return self.available_spots == 0
