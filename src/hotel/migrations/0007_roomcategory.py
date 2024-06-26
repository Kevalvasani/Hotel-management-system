# Generated by Django 4.2.10 on 2024-02-12 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hotel", "0006_delete_roomcategory"),
    ]

    operations = [
        migrations.CreateModel(
            name="RoomCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
                (
                    "person",
                    models.CharField(max_length=255, null=True, verbose_name="Person"),
                ),
                ("price", models.FloatField(null=True, verbose_name="Price")),
                ("image", models.ImageField(upload_to="hotel_image/")),
                (
                    "hotel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="roomcategories",
                        to="hotel.hotel",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
