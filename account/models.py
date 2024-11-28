from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', self.model.JobSpecialty.MANAGER)  

        if extra_fields.get('role') != self.model.JobSpecialty.MANAGER:
            raise ValueError('Superuser must have role="Manager".')
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    class JobSpecialty(models.TextChoices):
        MANAGER = "M", _("Manager")  
        SUPERVISOR = "S", _("Supervisor")  
        OPERATOR = "O", _("Operator")  
    
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', default="profile_pictures/default.jpeg"
    )
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=JobSpecialty.choices, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']

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
