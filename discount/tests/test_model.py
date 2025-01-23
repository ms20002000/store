from django.test import TestCase
from discount.models import Discount, Coupon
from account.models import CustomUser
from django.utils.timezone import now, timedelta

class DiscountModelTests(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(
            discount=20,
            start_date=now(),
            expire_at=now() + timedelta(days=30),
            max_amount=100
        )

    def test_discount_creation(self):
        self.assertEqual(Discount.objects.count(), 1)
        self.assertEqual(self.discount.discount, 20)

class CouponModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            password="testpassword"
        )
        self.coupon = Coupon.objects.create(
            amount=10,
            start_date=now(),
            expire_at=now() + timedelta(days=30),
            user=self.user
        )

    def test_coupon_creation(self):
        self.assertEqual(Coupon.objects.count(), 1)
        self.assertEqual(self.coupon.amount, 10)
        self.assertFalse(self.coupon.is_used)

    def test_coupon_mark_as_used(self):
        self.coupon.mark_as_used()
        self.assertTrue(self.coupon.is_used)
