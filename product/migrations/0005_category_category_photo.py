# Generated by Django 5.1.3 on 2024-12-15 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_remove_category_category_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_photo',
            field=models.ImageField(default='categories/default.jpg', upload_to='categories/'),
        ),
    ]
