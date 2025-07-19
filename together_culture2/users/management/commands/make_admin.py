from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Make a user an admin'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to make admin')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            user.role = User.ADMIN
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully made {username} an admin')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User {username} does not exist')
            ) 