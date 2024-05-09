# Generated by Django 4.2.10 on 2024-02-13 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hotel", "0010_roomcategory_rooms"),
        ("booking", "0002_alter_booking_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="hotel",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="booking",
                to="hotel.hotel",
            ),
        ),
    ]
