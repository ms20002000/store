from django.db import models
from core.models import BaseModel
from account.models import Account
from product.models import Product

class Order(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    discount_code = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
