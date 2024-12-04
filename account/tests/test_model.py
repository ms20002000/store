from django.test import TestCase
from account.models import CustomUser

class CustomUserModelExtendedTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number="1234567890",
            password="password123",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            role=CustomUser.JobSpecialty.CUSTOMER
        )
        self.superuser = CustomUser.objects.create_superuser(
            phone_number="0987654321",
            password="admin123"
        )

    def test_user_creation_without_phone_number(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(phone_number=None, password="password123")

    def test_superuser_creation_with_wrong_role(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                phone_number="1112223333",
                password="admin123",
                role=CustomUser.JobSpecialty.OPERATOR
            )

    def test_is_manager_property(self):
        self.assertFalse(self.user.is_manager)
        self.assertTrue(self.superuser.is_manager)

    def test_is_supervisor_property(self):
        self.assertFalse(self.user.is_supervisor)

    def test_is_operator_property(self):
        self.assertFalse(self.user.is_operator)

    def test_user_update(self):
        self.user.first_name = "Jane"
        self.user.last_name = "Smith"
        self.user.save()
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(self.user.last_name, "Smith")

    def test_string_representation(self):
        self.assertEqual(str(self.user), "1234567890")
        self.assertEqual(str(self.superuser), "0987654321")

    def test_required_fields(self):
        self.assertEqual(self.user.USERNAME_FIELD, "phone_number")
        self.assertIn("first_name", self.user.REQUIRED_FIELDS)
        self.assertIn("last_name", self.user.REQUIRED_FIELDS)
        self.assertIn("email", self.user.REQUIRED_FIELDS)

    def test_default_role(self):
        new_user = CustomUser.objects.create_user(
            phone_number="2223334444",
            password="test1234"
        )
        self.assertEqual(new_user.role, CustomUser.JobSpecialty.CUSTOMER)

    def test_default_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_user_permissions(self):
        self.assertTrue(self.superuser.is_superuser)
