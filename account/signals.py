from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from account.models import CustomUser

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    supervisor_group, _ = Group.objects.get_or_create(name='Supervisor')
    operator_group, _ = Group.objects.get_or_create(name='Operator')
    customer_group, _ = Group.objects.get_or_create(name='Customer')

    permissions = Permission.objects.filter(
        codename__in=['add_product', 'change_product', 'delete_product', 'add_category', 'change_category', 'delete_category', 'add_discount', 'change_discount', 'delete_discount',
                      'add_productfile', 'change_productfile', 'delete_productfile', 'add_topicfile', 'change_topicfile', 'delete_topicfile', 'add_topicmedia', 'change_topicmedia', 'delete_topicmedia']
    )
    manager_group.permissions.set(permissions)
    manager_group.save()

    operator_permissions = Permission.objects.filter(
        codename__in=['add_customer', 'change_customer', 'delete_customer', 'add_order', 'change_order', 'delete_order']
    )
    operator_group.permissions.set(operator_permissions)
    operator_group.save()

    supervisor_permissions = Permission.objects.filter(codename__startswith='view_')
    supervisor_group.permissions.set(supervisor_permissions)
    supervisor_group.save()


@receiver(post_save, sender=CustomUser)
def assign_group(sender, instance, created, **kwargs):
    instance.groups.clear()

    if instance.role == CustomUser.JobSpecialty.MANAGER:
        group = Group.objects.get(name='Manager')
    elif instance.role == CustomUser.JobSpecialty.SUPERVISOR:
        group = Group.objects.get(name='Supervisor')
    elif instance.role == CustomUser.JobSpecialty.OPERATOR:
        group = Group.objects.get(name='Operator')
    else:
        group = Group.objects.get(name='Customer')

    instance.groups.add(group)
