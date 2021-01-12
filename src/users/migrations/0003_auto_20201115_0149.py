# Generated by Django 3.1.2 on 2020-11-15 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_auto_20201115_0048"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.CharField(
                db_index=True,
                max_length=255,
                unique=True,
                verbose_name="Адрес электронной почты",
            ),
        ),
    ]
