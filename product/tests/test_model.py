from django.test import TestCase
from product.models import Category, Product, Attributes

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            brand="BrandX",
            price=499.99,
            description="A high-quality smartphone.",
            stock_quantity=50,
            category=self.category
        )
        self.attribute = Attributes.objects.create(name="Color", value="Black")

    def test_category_creation(self):
        self.assertEqual(str(self.category), "Electronics")

    def test_product_creation(self):
        self.assertEqual(str(self.product), "Smartphone (BrandX)")
        self.assertEqual(self.product.stock_quantity, 50)

    def test_attribute_creation(self):
        self.assertEqual(str(self.attribute), "Color: Black")
