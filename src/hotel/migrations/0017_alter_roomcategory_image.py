# Generated by Django 5.0.2 on 2024-03-10 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0016_rename_roomcategory_roomcategoryimage_roomcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomcategory',
            name='image',
            field=models.ImageField(blank=True, upload_to='hotel_image/'),
        ),
    ]
