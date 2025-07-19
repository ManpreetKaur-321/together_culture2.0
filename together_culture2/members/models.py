from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from tags.models import Tag

class MembershipType(models.Model):
    MEMBERSHIP_CHOICES = [
        ('community', 'Community Members'),
        ('key_access', 'Key Access Members'),
        ('creative_workspace', 'Creative Workspace Members'),
    ]
    
    name = models.CharField(max_length=50, unique=True)
    membership_category = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default='community')
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False, help_text="Set as default for new members")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration_months = models.IntegerField(default=12, help_text="Duration in months")
    benefits_list = models.TextField(blank=True, help_text="List of benefits for this membership type")
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # If this is being set as default, unset other defaults
        if self.is_default:
            MembershipType.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

class Benefit(models.Model):
    BENEFIT_TYPES = [
        ('event_access', 'Event Access'),
        ('digital_content', 'Digital Content'),
        ('workspace_access', 'Workspace Access'),
        ('networking', 'Networking'),
        ('training', 'Training'),
        ('mentoring', 'Mentoring'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    benefit_type = models.CharField(max_length=20, choices=BENEFIT_TYPES)
    membership_types = models.ManyToManyField(MembershipType, related_name='available_benefits')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class MemberBenefitUsage(models.Model):
    member = models.ForeignKey('MemberProfile', on_delete=models.CASCADE, related_name='benefit_usage')
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('member', 'benefit', 'used_at')
    
    def __str__(self):
        return f"{self.member.user.username} - {self.benefit.name}"

class MemberProfile(models.Model):
    INTEREST_CHOICES = [
        ('caring', 'Caring'),
        ('sharing', 'Sharing'),
        ('creating', 'Creating'),
        ('experiencing', 'Experiencing'),
        ('working', 'Working'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Authorization'),
        ('authorized', 'Authorized'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interests = models.CharField(max_length=100, choices=INTEREST_CHOICES)
    membership_type = models.ForeignKey(MembershipType, on_delete=models.SET_NULL, null=True, blank=True)
    orientation_info = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    bio = models.TextField(blank=True, help_text="Personal bio or description")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='member_profiles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    authorized_at = models.DateTimeField(null=True, blank=True)
    authorized_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='authorized_members')

    def __str__(self):
        return f"Profile: {self.user.username}"
    
    @property
    def is_authorized(self):
        return self.status == 'authorized'
    
    def get_available_benefits(self):
        """Get benefits available to this member based on their membership type"""
        if self.membership_type:
            return Benefit.objects.filter(
                membership_types=self.membership_type,
                is_active=True
            )
        return Benefit.objects.none()
    
    def get_used_benefits(self):
        """Get benefits this member has used"""
        return self.benefit_usage.all()
    
    def get_unused_benefits(self):
        """Get benefits this member hasn't used yet"""
        used_benefit_ids = self.benefit_usage.values_list('benefit_id', flat=True)
        return self.get_available_benefits().exclude(id__in=used_benefit_ids)
    
    def get_default_membership_type(self):
        """Get the default membership type or create one if none exists"""
        default_type = MembershipType.objects.filter(is_default=True).first()
        if not default_type:
            # Create a default Community Members membership type if none exists
            default_type = MembershipType.objects.create(
                name="Community Members",
                membership_category='community',
                description="Default community membership for new members",
                is_default=True,
                price=0.00,
                duration_months=12,
                benefits_list="• Access to community events\n• Basic digital content\n• Community networking"
            )
        return default_type

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.MEMBER:
        # Get or create default Community Members membership type
        default_membership = MembershipType.objects.filter(is_default=True).first()
        if not default_membership:
            default_membership = MembershipType.objects.create(
                name="Community Members",
                membership_category='community',
                description="Default community membership for new members",
                is_default=True,
                price=0.00,
                duration_months=12,
                benefits_list="• Access to community events\n• Basic digital content\n• Community networking"
            )
        
        MemberProfile.objects.create(
            user=instance,
            membership_type=default_membership
        )
