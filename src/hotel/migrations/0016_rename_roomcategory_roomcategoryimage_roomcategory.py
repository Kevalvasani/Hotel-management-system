# Generated by Django 5.0.2 on 2024-03-09 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0015_roomcategoryimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomcategoryimage',
            old_name='Roomcategory',
            new_name='roomcategory',
        ),
    ]
