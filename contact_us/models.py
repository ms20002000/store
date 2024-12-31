from django.db import models
from core.models import BaseModel


class ContactUs(BaseModel):
    class JobSpecialty(models.TextChoices):
        TEACHER = "T", ("Teacher")  
        STUDENT = "S", ("Student")  

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=50, unique=True)
    role = models.CharField(max_length=50, choices=JobSpecialty.choices)
    message = models.TextField(max_length=5000)
    resume = models.FileField(upload_to='contact_us/', blank=True, null=True)
