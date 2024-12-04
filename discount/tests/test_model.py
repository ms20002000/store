from django.test import TestCase
from discount.models import Discount
from datetime import datetime, timedelta

class DiscountModelTest(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(
            discount=10,
            expire_at=datetime.now() + timedelta(days=5),
            max_amount=100
        )

    def test_discount_creation(self):
        self.assertEqual(self.discount.discount, 10)
        self.assertEqual(self.discount.max_amount, 100)
        self.assertTrue(self.discount.expire_at > datetime.now())
