# Generated by Django 5.1.3 on 2024-12-24 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0002_discount_discount_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('start_date', models.DateTimeField()),
                ('expire_at', models.DateTimeField()),
                ('min_price', models.PositiveIntegerField(blank=True, null=True)),
                ('max_amount', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='discount',
            name='discount_type',
        ),
        migrations.AddField(
            model_name='discount',
            name='start_date',
            field=models.DateTimeField(default='2024-12-02 12:20'),
            preserve_default=False,
        ),
    ]
