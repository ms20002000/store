# Generated by Django 5.1.3 on 2025-01-11 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_payment_method_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='is_deleted',
        ),
    ]
