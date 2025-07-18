from django.db import models
from events.models import Event
from members.models import MemberProfile

# Create your models here.

class Booking(models.Model):
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.user.username} booked {self.event.title}"
