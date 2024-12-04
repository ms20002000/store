from django.test import TestCase
from account.models import CustomUser
from product.models import Product, Category
from order.models import Order, OrderItem

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number="1234567890",
            password="password123"
        )
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            brand="BrandX",
            price=499.99,
            stock_quantity=50,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            status="pending",
            payment_method="credit_card",
            address="123 Main St"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )

    def test_order_creation(self):
        self.assertEqual(str(self.order), f"Order {self.order.id} - pending")

    def test_order_item_creation(self):
        self.assertEqual(str(self.order_item), f"2 x Smartphone (Order {self.order.id})")
        self.assertEqual(self.order_item.quantity, 2)
