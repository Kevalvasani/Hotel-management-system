# Generated by Django 5.0.2 on 2024-02-10 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('owner_name', models.CharField(max_length=255, null=True, verbose_name='Owner name')),
                ('services', models.TextField(null=True, verbose_name='Servises')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('rattings', models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Rattings')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('city', models.CharField(max_length=255, verbose_name='City')),
                ('image', models.ImageField(upload_to='hotel_image/')),
                ('room', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('available_rooms', models.IntegerField(null=True)),
                ('booked_rooms', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='hotel_image/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('person', models.CharField(max_length=255, null=True, verbose_name='Person')),
                ('price', models.FloatField(null=True, verbose_name='Price')),
                ('image', models.ImageField(upload_to='hotel_image/')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roomcategories', to='hotel.hotel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
