from django.db import models
from core.models import BaseModel

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

    def __str__(self):
        return str(self.amount)