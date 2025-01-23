from django.core.management.base import BaseCommand
from account.models import CustomUser
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Create a user with a specific role"

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help="The email address of the user")
        parser.add_argument('first_name', type=str, help="The first name of the user")
        parser.add_argument('last_name', type=str, help="The last name of the user")
        parser.add_argument('phone_number', type=str, help="The phone number of the user")
        parser.add_argument('role', type=str, help="The role of the user (Manager, Supervisor, Operator, Customer)")
        parser.add_argument('password', type=str, help="Password for the user (optional)")

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        phone_number = kwargs['phone_number']
        role = kwargs['role'].capitalize() 
        password = kwargs['password']

        # Check if the role is valid
        if role not in ['Manager', 'Supervisor', 'Operator']:
            self.stdout.write(self.style.ERROR(f"Invalid role: {role}. Choose from Manager, Supervisor, Operator."))
            return
        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR('User with this email already exists.'))
            return

        # Create the user
        user = CustomUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role[:1],
            password=password,
            is_staff=True,
        )

        # Assign the user to the corresponding group
        group = Group.objects.get(name=role)
        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(f"User {email} with role {role} created successfully."))
