from django.db import models
from core.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255)
    photo_url = models.URLField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    photo_url = models.URLField(null=True, blank=True)
    discount = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.name} ({self.brand})"
