from django.test import TestCase
from product.models import Category, Product

class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category 1")
        self.product = Product.objects.create(
            name="Test Product",
            teacher="John Doe",
            price=100.00,
            description="Test Description",
            category=self.category,
            course_time="01:30:00",
            prerequisite="None"
        )

    def test_category_creation(self):
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(self.category.name, "Category 1")

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.teacher, "John Doe")
        self.assertEqual(self.product.category.name, "Category 1")
