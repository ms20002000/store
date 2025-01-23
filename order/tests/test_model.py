from django.test import TestCase
from order.models import Order, OrderItem
from account.models import CustomUser
from product.models import Product, Category
from discount.models import Coupon

class OrderModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="testuser@example.com", 
            first_name="Test", 
            last_name="User", 
            phone_number="1234567890"
        )
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
        self.coupon = Coupon.objects.create(
            amount=10,
            start_date="2025-01-01 00:00:00",
            expire_at="2025-12-31 23:59:59",
            user=self.user
        )
        self.order = Order.objects.create(
            user=self.user,
            status="completed",
            coupon=self.coupon,
            total_price=90.00
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=90.00
        )

    def test_order_creation(self):
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.status, "completed")
        self.assertEqual(self.order.total_price, 90.00)
    
    def test_order_item_creation(self):
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(self.order_item.product.name, "Test Product")
        self.assertEqual(self.order_item.price, 90.00)
