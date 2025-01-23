from django.db import models
from core.models import BaseModelWithoutDelete
from account.models import CustomUser as Account
from product.models import Product
from discount.models import Coupon

class Order(BaseModelWithoutDelete):
    """
    Represents an order made by a user.

    Attributes:
        STATUS_CHOICES (tuple): Choices for the status of the order, either 'completed' or 'cancelled'.
        user (Account): A foreign key linking the order to the user who placed it.
        status (str): The current status of the order, restricted to predefined choices.
        coupon (Coupon): A foreign key linking the order to an applied coupon, if any. Optional.
        total_price (float): The total price of the order.

    Methods:
        __str__(): Returns a string representation of the order, including its ID and status.
    """
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    coupon = models.ForeignKey(Coupon, on_delete=models.DO_NOTHING, null=True, blank=True)
    total_price = models.FloatField()

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(BaseModelWithoutDelete):
    """
    Represents an individual item within an order.

    Attributes:
        order (Order): A foreign key linking the item to its associated order.
        product (Product): A foreign key linking the item to the product being purchased.
        price (float): The price of the product at the time of the order.

    Methods:
        __str__(): Returns a string representation of the item, including the product name and associated order ID.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} (Order {self.order.id})"
