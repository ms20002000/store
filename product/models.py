from django.db import models
from core.models import BaseModel
from discount.models import Discount
from django.core.validators import URLValidator



class Category(BaseModel):
    """
    Represents a product category in the system.

    Attributes:
        name (str): The unique name of the category.
        parent (Category): A self-referential foreign key to represent parent categories.
        category_photo (str): A URL for the category photo. Defaults to a placeholder image.

    Methods:
        __str__(): Returns the string representation of the category, which is its name.
    """
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    category_photo = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        validators=[URLValidator()],
        default="https://res.cloudinary.com/dodrvhrz7/image/upload/v1735037850/default_gseslf.jpg"
    )

    def __str__(self):
        return self.name

class Product(BaseModel):
    """
    Represents a product, such as an educational course or item, in the system.

    Attributes:
        name (str): The unique name of the product.
        teacher (str): The teacher or presenter associated with the product.
        price (Decimal): The price of the product, stored with two decimal places.
        description (str): A detailed description of the product.
        category (Category): A foreign key to the `Category` to which the product belongs.
        discount (Discount): A foreign key to the `Discount` applied to the product. Optional.
        course_time (time): The duration of the course.
        prerequisite (str): Any prerequisite required for the product or course.

    Methods:
        __str__(): Returns the string representation of the product, which is its name.
    """
    name = models.CharField(max_length=255, unique=True)
    teacher = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    discount = models.ForeignKey(Discount, on_delete=models.DO_NOTHING, null=True, blank=True) 
    course_time = models.TimeField()
    prerequisite = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    
class ProductFile(BaseModel):
    """
    Represents additional files or media associated with a product.

    Attributes:
        product_movie (str): A URL for the product video. Optional.
        product_photo (str): A URL for the product photo. Optional.
        product (Product): A foreign key linking the file to its associated product.
    """
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
    """
    Represents files or documents associated with a specific product topic.

    Attributes:
        title (str): The unique title of the topic file.
        description (str): A detailed description of the topic file.
        product (Product): A foreign key linking the topic file to its associated product.
        topic_photo (str): A URL for the topic photo. Optional.
    """
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='topic_file')
    topic_photo = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        validators=[URLValidator()]
    )

class TopicMedia(BaseModel):
    """
    Represents media content associated with a specific topic file.

    Attributes:
        title (str): The unique title of the topic media.
        description (str): A detailed description of the topic media.
        topic_file (TopicFile): A foreign key linking the media to its associated topic file.
        topic_movie (str): A URL for the topic video. Optional.
    """
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    topic_file = models.ForeignKey(TopicFile, on_delete=models.CASCADE, related_name='topic_media')
    topic_movie = models.URLField(
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