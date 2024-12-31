from django.db import models
from core.models import BaseModel
from account.models import CustomUser as Account
from product.models import Product
from discount.models import Coupon

class Order(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    coupon = models.ForeignKey(Coupon, on_delete=models.DO_NOTHING, null=True, blank=True)
    total_price = models.FloatField()

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} (Order {self.order.id})"
