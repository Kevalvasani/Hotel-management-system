# Generated by Django 5.0.2 on 2024-03-14 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_guest_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='first_name',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='last_name',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
    ]
