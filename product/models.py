from django.db import models
from core.models import BaseModel
from discount.models import Discount
from django.core.validators import URLValidator


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    # category_photo = models.ImageField(upload_to='categories/', default='categories/default.jpg')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    category_photo = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        validators=[URLValidator()],
        default="https://127.0.0.1/media/categories/default.jpg"
    )

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    teacher = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    discount = models.ForeignKey(Discount, on_delete=models.DO_NOTHING, null=True, blank=True) 
    course_time = models.TimeField()
    prerequisite = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.brand})"

    
class ProductFile(BaseModel):
    product_movie = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        validators=[URLValidator()]
    )
    product_photo = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        validators=[URLValidator()]
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_file')

    
class TopicFile(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='topic_file')
    product_movie = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        validators=[URLValidator()]
    )
    product_photo = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        validators=[URLValidator()]
    )


class Attributes(BaseModel):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ManyToManyField(Product, related_name='attributes')
    

    def __str__(self):
        return f"{self.name}: {self.value}"