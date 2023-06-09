# Generated by Django 4.1.7 on 2023-05-30 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feed",
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
                ("content", models.TextField()),
                ("image", models.TextField()),
                ("email", models.EmailField(default="", max_length=254)),
                ("like_count", models.IntegerField()),
            ],
        ),
    ]
