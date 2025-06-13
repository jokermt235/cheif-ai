from django.core.management.base import BaseCommand
from storage.models import User

class Command(BaseCommand):
    help = 'Manage user  operations'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='enter username name here or email')
        parser.add_argument('password', type=str, help='enter password name here')
        

    def handle(self, *args, **options):
        username = options['username']
        passwrd = options['password']
       
        if(User.objects.create_user(email=username, password=passwrd)):
            self.stdout.write(self.style.SUCCESS(f'Congratulations!You just created the new user!'))
        else:
            self.stdout.write(self.style.SUCCESS(f'User was not created'))