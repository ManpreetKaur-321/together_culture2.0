from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User

class MembershipType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class MemberProfile(models.Model):
    INTEREST_CHOICES = [
        ('caring', 'Caring'),
        ('sharing', 'Sharing'),
        ('creating', 'Creating'),
        ('experiencing', 'Experiencing'),
        ('working', 'Working'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interests = models.CharField(max_length=100, choices=INTEREST_CHOICES)
    membership_type = models.ForeignKey(MembershipType, on_delete=models.SET_NULL, null=True, blank=True)
    orientation_info = models.TextField(blank=True)
    is_authorized = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile: {self.user.username}"

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.MEMBER:
        MemberProfile.objects.create(user=instance)
