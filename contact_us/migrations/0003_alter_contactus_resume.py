# Generated by Django 5.1.3 on 2024-12-31 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_us', '0002_rename_full_name_contactus_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='contact_us/'),
        ),
    ]
