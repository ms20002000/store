from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
import random, json
from redis import Redis


class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    class JobSpecialty(models.TextChoices):
        MANAGER = "M", _("Manager")  
        SUPERVISOR = "S", _("Supervisor")  
        OPERATOR = "O", _("Operator")  
        CUSTOMER = "C", _("Customer")
    
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=50)
    profile_picture = models.ImageField(
        upload_to='accounts/', default="accounts/default.jpg"
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
    

class OTPCode(BaseModel):
    email = models.EmailField()
    code = models.CharField(max_length=6)

    @classmethod
    def run_redis(cls):
        redis_client = Redis(host='localhost', port=6379, db=0)
        return redis_client

    @classmethod
    def save_otp_to_redis(cls, email, otp_code):
        redis_client = cls.run_redis()
        redis_client.set(f'otp_{email}', otp_code, ex=600)
        

    @classmethod
    def save_user_data_to_redis(cls, email, data):
        redis_client = cls.run_redis()
        data_json = json.dumps(data)
        redis_client.set(f'user_data_{email}', data_json, ex=600)
    
    @classmethod
    def get_otp_code(cls, email):
        redis_client = cls.run_redis()
        return redis_client.get(f'otp_{email}')
    
    @classmethod
    def get_user_data(cls, email):
        redis_client = cls.run_redis()
        user_data = redis_client.get(f'user_data_{email}')
        if user_data:
            return json.loads(user_data.decode()) 
        return None

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))