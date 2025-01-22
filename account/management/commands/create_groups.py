from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from product.models import Product, Category, Discount 
from order.models import Order


class Command(BaseCommand):
    help = 'Create initial groups and permissions'

    def handle(self, *args, **kwargs):
        # Create groups
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        supervisor_group, _ = Group.objects.get_or_create(name='Supervisor')
        operator_group, _ = Group.objects.get_or_create(name='Operator')

        # Get or create permissions
        product_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Product))
        category_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Category))
        discount_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Discount))
        # customer_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Customer))
        order_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Order))
    
        # Assign permissions to groups
        manager_group.permissions.set(product_permissions | category_permissions | discount_permissions)
        supervisor_group.permissions.set(Permission.objects.all())  # Full access
        # operator_group.permissions.set(customer_permissions | order_permissions)

        self.stdout.write(self.style.SUCCESS('Groups and permissions have been set up'))
