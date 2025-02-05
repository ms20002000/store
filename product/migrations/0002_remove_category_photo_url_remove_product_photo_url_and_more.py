# Generated by Django 5.1.3 on 2024-12-11 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='photo_url',
        ),
        migrations.RemoveField(
            model_name='product',
            name='photo_url',
        ),
        migrations.AddField(
            model_name='category',
            name='category_photo',
            field=models.ImageField(default='categorys/default.jpg', upload_to='categorys/'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_photo',
            field=models.ImageField(default='products/default.jpg', upload_to='products/'),
        ),
    ]
