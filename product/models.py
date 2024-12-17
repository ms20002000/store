from django.db import models
from core.models import BaseModel
from discount.models import Discount

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    category_photo = models.ImageField(upload_to='categories/', default='categories/default.jpg')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    brand = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_photo = models.ImageField(upload_to='products/', default='products/default.jpg')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True) 

    def __str__(self):
        return f"{self.name} ({self.brand})"


class Attributes(BaseModel):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: {self.value}"