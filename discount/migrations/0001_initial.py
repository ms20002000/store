# Generated by Django 5.1.3 on 2024-11-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('discount', models.IntegerField(blank=True, null=True)),
                ('expire_at', models.DateTimeField()),
                ('max_amount', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
