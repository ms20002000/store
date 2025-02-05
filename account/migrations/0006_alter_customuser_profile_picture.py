# Generated by Django 5.1.3 on 2024-12-31 10:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.URLField(blank=True, default='https://www.defineinternational.com/wp-content/uploads/2014/06/dummy-profile.png', null=True, validators=[django.core.validators.URLValidator()]),
        ),
    ]
