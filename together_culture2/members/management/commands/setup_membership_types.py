from django.core.management.base import BaseCommand
from members.models import MembershipType

class Command(BaseCommand):
    help = 'Set up the three membership types: Community, Key Access, and Creative Workspace'

    def handle(self, *args, **options):
        # Clear existing membership types
        MembershipType.objects.all().delete()
        
        # Create Community Members (default)
        community = MembershipType.objects.create(
            name="Community Members",
            membership_category='community',
            description="Basic community membership with access to events and networking",
            is_default=True,
            price=0.00,
            duration_months=12,
            benefits_list="• Access to community events\n• Basic digital content\n• Community networking\n• Member directory access"
        )
        
        # Create Key Access Members
        key_access = MembershipType.objects.create(
            name="Key Access Members",
            membership_category='key_access',
            description="Enhanced membership with priority access and additional benefits",
            is_default=False,
            price=25.00,
            duration_months=12,
            benefits_list="• All Community Member benefits\n• Priority event booking\n• Exclusive workshops\n• Mentoring sessions\n• Advanced digital content"
        )
        
        # Create Creative Workspace Members
        creative_workspace = MembershipType.objects.create(
            name="Creative Workspace Members",
            membership_category='creative_workspace',
            description="Premium membership with workspace access and full benefits",
            is_default=False,
            price=50.00,
            duration_months=12,
            benefits_list="• All Key Access benefits\n• Workspace access\n• Equipment rental\n• Professional development\n• Project collaboration\n• Industry connections"
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created 3 membership types:\n'
                f'• {community.name} (Default)\n'
                f'• {key_access.name}\n'
                f'• {creative_workspace.name}'
            )
        ) 