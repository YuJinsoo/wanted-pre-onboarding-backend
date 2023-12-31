# Generated by Django 4.2.6 on 2023-10-14 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="JobOpening",
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
                ("country", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=100)),
                ("position", models.CharField(max_length=100)),
                ("content", models.TextField(max_length=500)),
                ("tech", models.CharField(max_length=100)),
                ("reward", models.PositiveIntegerField(default=0)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recruit.company",
                    ),
                ),
            ],
        ),
    ]
