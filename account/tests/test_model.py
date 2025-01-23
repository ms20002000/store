from django.test import TestCase
from account.models import CustomUser

class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            password="testpassword"
        )

    def test_user_creation(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("testpassword"))

    def test_user_role_default(self):
        self.assertEqual(self.user.role, CustomUser.JobSpecialty.CUSTOMER)
