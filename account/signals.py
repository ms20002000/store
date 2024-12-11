from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    manager_group, created = Group.objects.get_or_create(name='Manager')
    customer_group, _ = Group.objects.get_or_create(name='Customer')

    if created:
        permissions = Permission.objects.filter(codename__in=['add_product', 'change_product', 'delete_product'])
        manager_group.permissions.set(permissions)
        manager_group.save()
