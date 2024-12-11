from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    class JobSpecialty(models.TextChoices):
        MANAGER = "M", _("Manager")  
        SUPERVISOR = "S", _("Supervisor")  
        OPERATOR = "O", _("Operator")  
        CUSTOMER = "C", _("Customer")
    
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', default="profile_pictures/default.jpeg"
    )
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=JobSpecialty.choices, default=JobSpecialty.CUSTOMER)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

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