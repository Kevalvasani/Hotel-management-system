# Generated by Django 4.2.10 on 2024-03-18 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
