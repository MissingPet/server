# Generated by Django 3.1.2 on 2020-11-13 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("announcements", "0004_auto_20201113_2210"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="animal_type",
            field=models.IntegerField(
                choices=[(1, "Собака"), (2, "Кошка"), (3, "Другое")],
                verbose_name="Тип животного",
            ),
        ),
        migrations.AlterField(
            model_name="announcement",
            name="announcement_type",
            field=models.IntegerField(
                choices=[(1, "Потеряно"), (2, "Найдено")], verbose_name="Тип объявления"
            ),
        ),
    ]
