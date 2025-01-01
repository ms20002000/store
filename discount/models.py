from django.db import models
from core.models import BaseModel
import uuid
from django.utils.timezone import now


class Discount(BaseModel):
    discount = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField()
    expire_at = models.DateTimeField()
    max_amount = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.discount)


class Coupon(BaseModel):
    amount = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField()
    expire_at = models.DateTimeField()
    min_price = models.PositiveIntegerField(null=True, blank=True)
    max_amount = models.PositiveIntegerField(null=True, blank=True)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    is_used = models.BooleanField(default=False)


    def generate_unique_code(self):
        """
        Generates a unique code for the coupon.
        """
        while True:
            code = str(uuid.uuid4())[:8].upper()
            if not Coupon.objects.filter(code=code).exists():
                return code

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure a unique code is generated for the coupon.
        """
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def is_valid_for_user(self, user):
        """
        Check if the coupon is valid for the given user.
        """
        return (
            self.user == user and 
            not self.is_used and 
            self.start_date <= now() <= self.expire_at
        )

    def mark_as_used(self):
        """
        Mark the coupon as used.
        """
        self.is_used = True
        self.save()
    
    def __str__(self):
        return self.code if self.code else str(self.amount)