# Generated by Django 4.2.10 on 2024-02-12 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hotel", "0007_roomcategory"),
    ]

    operations = [
        migrations.DeleteModel(
            name="RoomCategory",
        ),
    ]