# Generated by Django 5.1.3 on 2024-12-24 11:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_category_category_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_photo',
            field=models.URLField(blank=True, default='https://res.cloudinary.com/dodrvhrz7/image/upload/v1735037850/default_gseslf.jpg', null=True, validators=[django.core.validators.URLValidator()]),
        ),
    ]
