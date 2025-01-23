from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.core.validators import URLValidator


class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    CustomUser model that represents a user in the application.

    This model extends `AbstractBaseUser` and `PermissionsMixin` to provide custom 
    authentication and permissions functionality. It includes additional fields 
    and properties tailored to the specific requirements of the application.

    Attributes:
        phone_number (str): Unique phone number for the user, used for identification.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Unique email address used as the username field for authentication.
        profile_picture (str): URL of the user's profile picture. Defaults to a placeholder image.
        address (str): Optional text field for the user's address.
        role (str): User's job specialty, with choices defined in `JobSpecialty`.
                    Defaults to "Customer".
        is_active (bool): Indicates whether the user account is active. Default is `True`.
        is_staff (bool): Indicates whether the user has staff privileges. Default is `False`.

    Enums:
        JobSpecialty (TextChoices):
            - MANAGER ("M"): Manager role.
            - SUPERVISOR ("S"): Supervisor role.
            - OPERATOR ("O"): Operator role.
            - CUSTOMER ("C"): Customer role (default).

    Properties:
        is_manager (bool): Returns `True` if the user is a manager, otherwise `False`.
        is_supervisor (bool): Returns `True` if the user is a supervisor, otherwise `False`.
        is_operator (bool): Returns `True` if the user is an operator, otherwise `False`.

    Class Attributes:
        USERNAME_FIELD (str): Field used as the unique identifier for authentication. Defaults to `email`.
        REQUIRED_FIELDS (list): Fields required for user creation, aside from `USERNAME_FIELD`.

    Methods:
        __str__():
            Returns the string representation of the user, which is their `phone_number`.

    Relationships:
        - Inherits functionality from `BaseModel`, `AbstractBaseUser`, and `PermissionsMixin`.
        - Uses a custom manager `CustomUserManager` for additional user model logic.
    """
    class JobSpecialty(models.TextChoices):
        MANAGER = "M", _("Manager")  
        SUPERVISOR = "S", _("Supervisor")  
        OPERATOR = "O", _("Operator")  
        CUSTOMER = "C", _("Customer")
    
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=50)
    profile_picture = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        validators=[URLValidator()],
        default="https://res.cloudinary.com/dodrvhrz7/image/upload/v1735643606/dummy-profile_duj4ez.png"
    )
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=JobSpecialty.choices, default=JobSpecialty.CUSTOMER)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    @property
    def is_manager(self):
        return self.role == self.JobSpecialty.MANAGER

    @property
    def is_supervisor(self):
        return self.role == self.JobSpecialty.SUPERVISOR

    @property
    def is_operator(self):
        return self.role == self.JobSpecialty.OPERATOR
    