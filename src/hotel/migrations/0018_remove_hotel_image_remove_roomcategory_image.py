# Generated by Django 4.2.10 on 2024-03-11 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hotel", "0017_alter_roomcategory_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hotel",
            name="image",
        ),
        migrations.RemoveField(
            model_name="roomcategory",
            name="image",
        ),
    ]
