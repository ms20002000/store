# Generated by Django 5.1.3 on 2024-12-17 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_category_category_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
