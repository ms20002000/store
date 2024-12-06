from django.db import models
from core.models import BaseModel

class Discount(BaseModel):
    discount = models.IntegerField(null=True, blank=True)
    expire_at = models.DateTimeField()
    max_amount = models.PositiveIntegerField(null=True, blank=True)
    discount_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.discount)